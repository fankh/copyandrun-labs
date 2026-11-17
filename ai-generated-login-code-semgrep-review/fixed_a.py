# 변형 A 수정본: 매개변수 바인딩, 해시 비교, 로컬 바인딩, 디버그 끄기
import os
import sqlite3
from flask import Flask, request
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
DB = "users_a.db"


def init_db():
    con = sqlite3.connect(DB)
    con.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, pw_hash TEXT)")
    con.execute("INSERT INTO users VALUES ('alice', ?)", (generate_password_hash("alice-pw-1"),))
    con.commit()
    con.close()


@app.route("/login", methods=["POST"])
def login():
    con = sqlite3.connect(DB)
    row = con.execute("SELECT pw_hash FROM users WHERE username = ?", (request.form["username"],)).fetchone()
    con.close()
    if row and check_password_hash(row[0], request.form["password"]):
        return "로그인 성공"
    return "로그인 실패", 401


if __name__ == "__main__":
    init_db()
    app.run(host="127.0.0.1", port=5000, debug=os.environ.get("FLASK_DEBUG") == "1")
