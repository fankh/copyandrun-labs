import os
import sqlite3
import uuid
from functools import wraps

from flask import Flask, abort, g, jsonify, request, send_from_directory, session
from werkzeug.security import check_password_hash, generate_password_hash

USERS = [
    (1, "alice", "alice-pw", "user"),
    (2, "carol", "carol-pw", "user"),
    (3, "admin", "admin-pw", "admin"),
]
ORDERS = [
    (1, 1, "키보드", 35000),
    (2, 1, "마우스", 18000),
    (3, 2, "모니터", 210000),
    (4, 2, "웹캠", 45000),
]


def init_db(path):
    if os.path.exists(path):
        os.remove(path)
    conn = sqlite3.connect(path)
    conn.executescript("""
    CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT UNIQUE,
                        password_hash TEXT, role TEXT);
    CREATE TABLE orders (id INTEGER PRIMARY KEY, owner_id INTEGER, item TEXT,
                         price INTEGER, ref TEXT UNIQUE);
    """)
    conn.executemany("INSERT INTO users VALUES (?, ?, ?, ?)",
                     [(i, n, generate_password_hash(p), r) for i, n, p, r in USERS])
    conn.executemany("INSERT INTO orders VALUES (?, ?, ?, ?, ?)",
                     [(i, o, it, pr, uuid.uuid4().hex) for i, o, it, pr in ORDERS])
    conn.commit()
    conn.close()


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(g.app_db_path)
        g.db.row_factory = sqlite3.Row
    return g.db


def login_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if g.user is None:
            abort(401)
        return view(*args, **kwargs)
    return wrapper


def create_base(db_path):
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "dev-only-change-me"
    app.json.ensure_ascii = False  # 한글을 그대로 보이게 한다
    init_db(db_path)

    @app.before_request
    def load_user():
        g.app_db_path = db_path
        g.user = None
        if "user_id" in session:
            g.user = get_db().execute(
                "SELECT id, username, role FROM users WHERE id = ?",
                (session["user_id"],)).fetchone()

    @app.teardown_appcontext
    def close_db(exc):
        db = g.pop("db", None)
        if db is not None:
            db.close()

    @app.get("/")
    def index():
        return send_from_directory(os.path.dirname(os.path.abspath(__file__)), "index.html")

    @app.post("/login")
    def login():
        data = request.get_json(silent=True) or {}
        row = get_db().execute("SELECT * FROM users WHERE username = ?",
                               (data.get("username", ""),)).fetchone()
        if row is None or not check_password_hash(row["password_hash"],
                                                  data.get("password", "")):
            return jsonify(error="로그인 실패"), 401
        session.clear()
        session["user_id"] = row["id"]
        return jsonify(user=row["username"])

    @app.errorhandler(401)
    def unauthorized(e):
        return jsonify(error="로그인이 필요합니다"), 401

    @app.errorhandler(404)
    def not_found(e):
        # 이 예제의 404 는 모두 주문 조회에서 나오므로 같은 메시지를 쓴다
        return jsonify(error="없는 주문입니다"), 404

    return app
