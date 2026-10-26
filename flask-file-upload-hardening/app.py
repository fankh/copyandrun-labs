import os
import sqlite3
import uuid

from flask import Flask, request, send_from_directory
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.utils import secure_filename

BASE = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE, "uploads")
DB = os.path.join(BASE, "files.db")
ALLOWED = {"txt", "pdf", "png", "jpg", "jpeg"}

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 1 * 1000 * 1000  # 1MB
os.makedirs(UPLOAD_DIR, exist_ok=True)


def db():
    conn = sqlite3.connect(DB)
    conn.execute("CREATE TABLE IF NOT EXISTS files "
                 "(id TEXT PRIMARY KEY, original TEXT, stored TEXT)")
    return conn


def extension(name):
    if "." not in name:
        return ""
    return name.rsplit(".", 1)[1].lower()


@app.errorhandler(RequestEntityTooLarge)
def too_large(e):
    return "파일이 너무 큽니다. 1MB 이하만 올릴 수 있습니다.\n", 413


@app.route("/")
def index():
    return send_from_directory(BASE, "index.html")


@app.route("/upload", methods=["POST"])
def upload():
    f = request.files.get("file")
    if f is None or f.filename == "":
        return "파일이 없습니다.\n", 400

    original = secure_filename(f.filename) or "unnamed"
    ext = extension(f.filename)
    if ext not in ALLOWED:
        return "허용되지 않는 확장자입니다.\n", 400

    file_id = uuid.uuid4().hex
    stored = file_id + "." + ext
    path = os.path.realpath(os.path.join(UPLOAD_DIR, stored))
    if not path.startswith(os.path.realpath(UPLOAD_DIR) + os.sep):
        return "허용되지 않는 경로입니다.\n", 400
    f.save(path)

    conn = db()
    conn.execute("INSERT INTO files VALUES (?, ?, ?)", (file_id, original, stored))
    conn.commit()
    conn.close()
    return "저장: id=%s 원본=%s\n" % (file_id, original), 201


@app.route("/files/<file_id>")
def download(file_id):
    conn = db()
    row = conn.execute("SELECT original, stored FROM files WHERE id = ?",
                       (file_id,)).fetchone()
    conn.close()
    if row is None:
        return "파일이 없습니다.\n", 404
    resp = send_from_directory(UPLOAD_DIR, row[1], as_attachment=True,
                               download_name=row[0])
    resp.headers["X-Content-Type-Options"] = "nosniff"
    return resp


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=19202)
