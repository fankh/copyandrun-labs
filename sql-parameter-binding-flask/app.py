import os

from flask import Flask, jsonify, request, send_from_directory

import queries

BASE = os.path.dirname(os.path.abspath(__file__))


def create_app(db_path):
    app = Flask(__name__)

    @app.get("/")
    def index():
        return send_from_directory(BASE, "index.html")

    @app.get("/members")
    def members():
        name = request.args.get("name", "")
        sort = request.args.get("sort", "name")
        try:
            rows = queries.search_members(db_path, name, sort)
        except ValueError as e:
            return jsonify(error=str(e)), 400
        return jsonify([r["name"] for r in rows])

    @app.post("/login")
    def login():
        user = queries.find_user(
            db_path, request.form.get("username", ""), request.form.get("password", ""))
        if user is None:
            return jsonify(error="로그인 실패"), 401
        return jsonify(user=user["username"])

    return app


if __name__ == "__main__":
    queries.init_db("members.db")
    create_app("members.db").run(host="127.0.0.1", port=19800)
