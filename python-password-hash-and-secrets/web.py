import os
import sys

from flask import Flask, jsonify, request, send_from_directory

BASE = os.path.dirname(os.path.abspath(__file__))
folder = sys.argv[1] if len(sys.argv) > 1 else "after"
port = int(sys.argv[2]) if len(sys.argv) > 2 else 19700
sys.path.insert(0, os.path.join(BASE, folder))
import accounts  # noqa: E402

app = Flask(__name__)


@app.get("/")
def index():
    return send_from_directory(BASE, "index.html")


@app.post("/signup")
def signup():
    data = request.get_json(silent=True) or {}
    accounts.sign_up(data.get("name", ""), data.get("password", ""))
    return jsonify(ok=True)


@app.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    ok = accounts.log_in(data.get("name", ""), data.get("password", ""))
    return jsonify(ok=ok), (200 if ok else 401)


@app.get("/stored")
def stored():
    # 실습용: 저장된 값이 어떻게 생겼는지 보려고 그대로 내보낸다. 실제 서비스에서는 만들지 않는다.
    return jsonify(accounts.users)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=port)
