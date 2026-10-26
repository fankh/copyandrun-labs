import os
from flask import Flask, request, send_from_directory

app = Flask(__name__)
BASE = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.route("/")
def index():
    return send_from_directory(BASE, "index.html")


@app.route("/upload", methods=["POST"])
def upload():
    f = request.files.get("file")
    if f is None or f.filename == "":
        return "파일이 없습니다.\n", 400
    path = os.path.join(UPLOAD_DIR, f.filename)
    f.save(path)
    return "저장: %s\n" % os.path.relpath(path, BASE)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=19201)
