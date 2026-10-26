from flask import jsonify

from base import create_base, get_db, login_required


def create_app(db_path="vuln.db"):
    app = create_base(db_path)

    @app.get("/orders/<int:order_id>")
    @login_required
    def get_order(order_id):
        row = get_db().execute("SELECT * FROM orders WHERE id = ?",
                               (order_id,)).fetchone()
        if row is None:
            return jsonify(error="없는 주문입니다"), 404
        return jsonify(dict(row))

    return app


if __name__ == "__main__":
    create_app().run(host="127.0.0.1", port=19901)
