from functools import wraps

from flask import abort, g, jsonify, request

from base import create_base, get_db, login_required


def is_admin():
    return g.user["role"] == "admin"


# 열 이름을 문자열에 끼우지 않도록 쿼리 전체를 미리 적어 둔다 (관리자용, 일반 사용자용)
QUERIES = {
    "id": ("SELECT * FROM orders WHERE id = ?",
           "SELECT * FROM orders WHERE id = ? AND owner_id = ?"),
    "ref": ("SELECT * FROM orders WHERE ref = ?",
            "SELECT * FROM orders WHERE ref = ? AND owner_id = ?"),
}


def find_order(column, value):
    """소유자 조건을 쿼리에 넣는 유일한 곳. 관리자만 조건 없이 조회한다."""
    admin_sql, user_sql = QUERIES[column]
    if not is_admin():
        return get_db().execute(user_sql, (value, g.user["id"])).fetchone()
    return get_db().execute(admin_sql, (value,)).fetchone()


def owned_order(view):
    """주문 번호를 받는 모든 엔드포인트에 붙이는 데코레이터."""
    @wraps(view)
    @login_required
    def wrapper(order_id, *args, **kwargs):
        order = find_order("id", order_id)
        if order is None:
            abort(404)  # 없는 주문과 남의 주문을 같은 응답으로 돌려준다
        return view(order, *args, **kwargs)
    return wrapper


def create_app(db_path="fixed.db"):
    app = create_base(db_path)

    @app.get("/orders")
    @login_required
    def list_orders():
        if is_admin():
            rows = get_db().execute("SELECT * FROM orders").fetchall()
        else:
            rows = get_db().execute("SELECT * FROM orders WHERE owner_id = ?",
                                    (g.user["id"],)).fetchall()
        return jsonify([dict(r) for r in rows])

    @app.get("/orders/<int:order_id>")
    @owned_order
    def get_order(order):
        return jsonify(dict(order))

    @app.patch("/orders/<int:order_id>")
    @owned_order
    def update_order(order):
        item = (request.get_json(silent=True) or {}).get("item", "")
        db = get_db()
        db.execute("UPDATE orders SET item = ? WHERE id = ?", (item, order["id"]))
        db.commit()
        return jsonify(id=order["id"], item=item)

    @app.delete("/orders/<int:order_id>")
    @owned_order
    def delete_order(order):
        db = get_db()
        db.execute("DELETE FROM orders WHERE id = ?", (order["id"],))
        db.commit()
        return "", 204

    @app.get("/o/<ref>")
    @login_required
    def get_by_ref(ref):
        order = find_order("ref", ref)
        if order is None:
            abort(404)
        return jsonify(dict(order))

    return app


if __name__ == "__main__":
    create_app().run(host="127.0.0.1", port=19902)
