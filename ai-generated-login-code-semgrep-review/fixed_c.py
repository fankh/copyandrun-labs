# 변형 C 수정본: 무작위 토큰, 쿠키 플래그, 서버에 저장한 토큰으로 /admin 확인
import secrets
import sqlite3
from flask import Flask, make_response, request
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
DB = "users_c.db"
TOKENS = {}  # 토큰 -> 사용자 이름


def init_db():
    con = sqlite3.connect(DB)
    con.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, pw_hash TEXT, role TEXT)")
    con.execute("INSERT INTO users VALUES ('alice', ?, 'admin')", (generate_password_hash("alice-pw-1"),))
    con.execute("INSERT INTO users VALUES ('guest', ?, 'user')", (generate_password_hash("guest-pw-1"),))
    con.commit()
    con.close()


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    con = sqlite3.connect(DB)
    row = con.execute("SELECT pw_hash FROM users WHERE username = ?", (username,)).fetchone()
    con.close()
    if not row or not check_password_hash(row[0], request.form["password"]):
        return "로그인 실패", 401
    token = secrets.token_urlsafe(32)
    TOKENS[token] = username
    resp = make_response("로그인 성공")
    resp.set_cookie("auth_token", token, secure=True, httponly=True, samesite="Strict")
    return resp


@app.route("/admin")
def admin():
    if request.cookies.get("auth_token") in TOKENS:
        return "관리자 화면"
    return "권한 없음", 403


if __name__ == "__main__":
    init_db()
    app.run(host="127.0.0.1", port=5000)
