# 프롬프트 C 변형: "세션과 토큰까지 쓰는 Flask 로그인" (직접 작성한 연습용 코드)
import hashlib
import sqlite3
import time
from flask import Flask, make_response, request

app = Flask(__name__)
DB = "users_c.db"


def init_db():
    con = sqlite3.connect(DB)
    con.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, pw_hash TEXT)")
    con.execute("INSERT INTO users VALUES ('alice', ?)", (hashlib.sha256(b"alice-pw-1").hexdigest(),))
    con.commit()
    con.close()


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    pw_hash = hashlib.sha256(request.form["password"].encode()).hexdigest()
    con = sqlite3.connect(DB)
    row = con.execute("SELECT username FROM users WHERE username = ? AND pw_hash = ?", (username, pw_hash)).fetchone()
    con.close()
    if not row:
        return "로그인 실패", 401
    token = hashlib.md5(f"{username}{int(time.time())}".encode()).hexdigest()
    resp = make_response("로그인 성공")
    resp.set_cookie("auth_token", token)
    return resp


@app.route("/admin")
def admin():
    if request.args.get("admin") == "1":
        return "관리자 화면"
    return "권한 없음", 403


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
