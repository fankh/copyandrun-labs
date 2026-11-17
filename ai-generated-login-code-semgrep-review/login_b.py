# 프롬프트 B 변형: "비밀번호 저장까지 포함한 Flask 로그인" (직접 작성한 연습용 코드)
import hashlib
import sqlite3
from flask import Flask, request, session

app = Flask(__name__)
app.secret_key = "super-secret-key-1234"
DB = "users_b.db"


def init_db():
    con = sqlite3.connect(DB)
    con.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, pw_hash TEXT)")
    con.commit()
    con.close()


@app.route("/register", methods=["POST"])
def register():
    pw_hash = hashlib.md5(request.form["password"].encode()).hexdigest()
    con = sqlite3.connect(DB)
    con.execute("INSERT INTO users VALUES (?, ?)", (request.form["username"], pw_hash))
    con.commit()
    con.close()
    return "가입 완료"


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    pw_hash = hashlib.md5(request.form["password"].encode()).hexdigest()
    con = sqlite3.connect(DB)
    row = con.execute(f"SELECT username FROM users WHERE username = '{username}' AND pw_hash = '{pw_hash}'").fetchone()
    con.close()
    if row:
        session["user"] = row[0]
        return "로그인 성공"
    return "로그인 실패", 401


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
