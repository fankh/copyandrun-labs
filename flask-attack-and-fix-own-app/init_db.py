import os
import sqlite3

BASE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE, "app.db")

if os.path.exists(DB):
    os.remove(DB)
conn = sqlite3.connect(DB)
conn.executescript("""
CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT);
CREATE TABLE posts (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, body TEXT, author TEXT);
""")
conn.executemany("INSERT INTO users (username, password) VALUES (?, ?)",
                 [("admin", "s3cr3t-admin"), ("user", "user1234")])
conn.executemany("INSERT INTO posts (title, body, author) VALUES (?, ?, ?)",
                 [("공지사항", "실습용 게시판입니다.", "admin"),
                  ("환영합니다", "자유롭게 글을 남겨 보세요.", "user"),
                  ("점검 안내", "정기 점검이 예정되어 있습니다.", "admin")])
conn.commit()
conn.close()
print("created", DB)
