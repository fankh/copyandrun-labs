from vuln_app import create_app


def test_carol_cannot_read_alices_order(tmp_path):
    client = create_app(str(tmp_path / "t.db")).test_client()
    client.post("/login", json={"username": "carol", "password": "carol-pw"})
    res = client.get("/orders/1")  # 1번 주문은 alice 의 것
    assert res.status_code == 404, f"남의 주문이 보입니다: {res.get_json()}"
