# 변형 B 수정본: scrypt 해시, 매개변수 바인딩, 환경 변수의 secret_key
import os
import sqlite3
from flask import Flask, request, session
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = os.environ["SECRET_KEY"]
DB = "users_b.db"


def init_db():
    con = sqlite3.connect(DB)
    con.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, pw_hash TEXT)")
    con.commit()
    con.close()


@app.route("/register", methods=["POST"])
def register():
    pw_hash = generate_password_hash(request.form["password"], method="scrypt")
    con = sqlite3.connect(DB)
    con.execute("INSERT INTO users VALUES (?, ?)", (request.form["username"], pw_hash))
    con.commit()
    con.close()
    return "가입 완료"


@app.route("/login", methods=["POST"])
def login():
    con = sqlite3.connect(DB)
    row = con.execute("SELECT pw_hash FROM users WHERE username = ?", (request.form["username"],)).fetchone()
    con.close()
    if row is None:
        return "존재하지 않는 계정입니다", 401
    if not check_password_hash(row[0], request.form["password"]):
        return "비밀번호가 틀렸습니다", 401
    session["user"] = request.form["username"]
    return "로그인 성공"


if __name__ == "__main__":
    init_db()
    app.run(host="127.0.0.1", port=5000)
