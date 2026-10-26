import pytest

import queries
from app import create_app


@pytest.fixture
def client(tmp_path):
    db = str(tmp_path / "t.db")
    queries.init_db(db)
    queries.SQL_LOG.clear()
    return create_app(db).test_client()


def test_apostrophe_name_is_found(client):
    r = client.get("/members", query_string={"name": "O'Brien"})
    assert r.status_code == 200
    assert r.get_json() == ["O'Brien"]


def test_input_never_enters_sql_text(client):
    client.get("/members", query_string={"name": "O'Brien"})
    sql, params = queries.SQL_LOG[-1]
    assert "Brien" not in sql, "SQL 문장: " + sql
    assert any("Brien" in str(p) for p in params)


def test_login_apostrophe_password(client):
    r = client.post("/login", data={"username": "obrien", "password": "pw'x"})
    assert r.status_code == 401
    sql, params = queries.SQL_LOG[-1]
    assert "pw'x" not in sql, "SQL 문장: " + sql


def test_login_ok(client):
    r = client.post("/login", data={"username": "kim", "password": "pw-kim"})
    assert r.status_code == 200 and r.get_json() == {"user": "kim"}


def test_sort_allowlist(client):
    assert client.get("/members", query_string={"sort": "joined"}).get_json()[0] == "lee"
    assert client.get("/members", query_string={"sort": "nope"}).status_code == 400


def test_like_wildcard_is_literal(client):
    r = client.get("/members", query_string={"name": "_"})
    assert r.get_json() == ["a_b"]
