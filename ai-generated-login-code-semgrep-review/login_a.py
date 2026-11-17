# 프롬프트 A 변형: "Flask로 간단한 로그인 만들어 줘" (직접 작성한 연습용 코드, 실제 서비스에 쓰지 않습니다)
import sqlite3
from flask import Flask, request

app = Flask(__name__)
DB = "users_a.db"


def init_db():
    con = sqlite3.connect(DB)
    con.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")
    con.execute("INSERT INTO users VALUES ('alice', 'alice-pw-1')")
    con.commit()
    con.close()


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    con = sqlite3.connect(DB)
    query = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'"
    row = con.execute(query).fetchone()
    con.close()
    if row:
        return "로그인 성공"
    return "로그인 실패", 401


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
