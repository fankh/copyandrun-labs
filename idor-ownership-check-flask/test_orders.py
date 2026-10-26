import pytest

from app import create_app

PASSWORDS = {"alice": "alice-pw", "carol": "carol-pw", "admin": "admin-pw"}
# 주문 1, 2 는 alice, 3, 4 는 carol 의 것이다.
CASES = [
    # (사용자, 메서드, 주문 번호, 기대 상태)
    ("alice", "GET", 1, 200),
    ("alice", "GET", 3, 404),
    ("alice", "PATCH", 3, 404),
    ("alice", "DELETE", 3, 404),
    ("alice", "GET", 999, 404),
    ("carol", "GET", 1, 404),
    ("carol", "PATCH", 1, 404),
    ("carol", "DELETE", 1, 404),
    ("carol", "PATCH", 3, 200),
    ("carol", "DELETE", 4, 204),
    ("admin", "GET", 3, 200),
    ("admin", "PATCH", 1, 200),
    (None, "GET", 1, 401),
    (None, "DELETE", 1, 401),
]


@pytest.fixture
def make_client(tmp_path):
    app = create_app(str(tmp_path / "t.db"))  # 테스트 한 건에 앱과 DB 한 벌

    def make(user):
        client = app.test_client()
        if user:
            client.post("/login", json={"username": user, "password": PASSWORDS[user]})
        return client
    return make


@pytest.mark.parametrize("user,method,order_id,expected", CASES)
def test_access_matrix(make_client, user, method, order_id, expected):
    client = make_client(user)
    res = client.open(f"/orders/{order_id}", method=method, json={"item": "x"})
    assert res.status_code == expected


def test_list_contains_only_own_orders(make_client):
    ids = [o["id"] for o in make_client("alice").get("/orders").get_json()]
    assert ids == [1, 2]


def test_other_user_and_missing_look_the_same(make_client):
    client = make_client("alice")
    other = client.get("/orders/3")
    missing = client.get("/orders/999")
    assert (other.status_code, other.get_json()) == (missing.status_code, missing.get_json())


def test_knowing_the_uuid_is_not_enough(make_client):
    ref = make_client("admin").get("/orders/3").get_json()["ref"]
    assert make_client("alice").get(f"/o/{ref}").status_code == 404
    assert make_client("carol").get(f"/o/{ref}").status_code == 200
