import os
import sqlite3
from flask import Flask, request, session, redirect, send_file, render_template_string

app = Flask(__name__)
app.secret_key = "dev-insecure-key"
BASE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE, "app.db")
UPLOAD_DIR = os.path.join(BASE, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

LIST_HTML = """<h1>게시판</h1>
<ul>{% for p in posts %}<li>{{ p.id }}. <a href="/board/{{ p.id }}">{{ p.title }}</a> ({{ p.author }})</li>{% endfor %}</ul>"""

DETAIL_HTML = """<h2>{{ post.title }}</h2><p>작성자: {{ post.author }}</p><hr><div>{{ post.body }}</div>"""


def db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        conn = db()
        try:
            row = conn.execute(
                "SELECT * FROM users WHERE username = ? AND password = ?",
                (username, password)).fetchone()
        except sqlite3.Error as e:
            return "오류: %s" % e, 500
        finally:
            conn.close()
        if row:
            session["user"] = row["username"]
            return redirect("/board")
        return "로그인 실패", 200
    return '<form method="post"><input name="username"><input name="password" type="password"><button>로그인</button></form>'


@app.route("/board", methods=["GET", "POST"])
def board():
    conn = db()
    if request.method == "POST":
        if "user" not in session:
            conn.close()
            return redirect("/login")
        conn.execute("INSERT INTO posts (title, body, author) VALUES (?, ?, ?)",
                     (request.form.get("title", ""), request.form.get("body", ""), session["user"]))
        conn.commit()
    posts = conn.execute("SELECT * FROM posts ORDER BY id DESC").fetchall()
    conn.close()
    return render_template_string(LIST_HTML, posts=posts)


@app.route("/board/<int:post_id>")
def post_detail(post_id):
    conn = db()
    post = conn.execute("SELECT * FROM posts WHERE id = ?", (post_id,)).fetchone()
    conn.close()
    if not post:
        return "글을 찾을 수 없습니다.", 404
    return render_template_string(DETAIL_HTML, post=post)


@app.route("/download")
def download():
    filename = request.args.get("file", "")
    real = os.path.realpath(os.path.join(UPLOAD_DIR, filename))
    if not real.startswith(os.path.realpath(UPLOAD_DIR) + os.sep):
        return "허용되지 않는 경로입니다.", 403
    if not os.path.exists(real):
        return "파일이 없습니다.", 404
    return send_file(real)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
