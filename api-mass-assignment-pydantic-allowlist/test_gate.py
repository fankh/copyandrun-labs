"""대량 할당 회귀 방지 게이트입니다.

사용: pytest -q test_gate.py             (수정판 fixed_app 검사)
      APP_MODULE=vulnerable_app pytest -q test_gate.py   (취약판이 걸리는지 확인)
"""
import importlib
import os

import pytest
from fastapi.testclient import TestClient

mod = importlib.import_module(os.environ.get("APP_MODULE", "fixed_app"))
client = TestClient(mod.app)
ALICE = {"X-User": "alice"}


@pytest.fixture(autouse=True)
def fresh_data():
    mod.seed()


def test_allowed_fields_still_work():
    r = client.patch("/users/me", json={"display_name": "Alice K"}, headers=ALICE)
    assert r.status_code == 200
    assert r.json()["display_name"] == "Alice K"


@pytest.mark.parametrize("field,value", [("role", "admin"), ("is_admin", True),
                                         ("api_key", "stolen"), ("username", "root")])
def test_forbidden_fields_are_rejected(field, value):
    r = client.patch("/users/me", json={field: value}, headers=ALICE)
    assert r.status_code == 422
    assert r.json()["detail"][0]["type"] == "extra_forbidden"


@pytest.mark.parametrize("field", ["display_name", "team"])
def test_null_value_is_rejected(field):
    r = client.patch("/users/me", json={field: None}, headers=ALICE)
    assert r.status_code == 422
    assert client.get("/users/me", headers=ALICE).status_code == 200


def test_mixed_body_changes_nothing():
    r = client.patch("/users/me", json={"display_name": "Mallory", "role": "admin"}, headers=ALICE)
    assert r.status_code == 422
    assert mod.USERS["alice"]["display_name"] == "Alice"


def test_role_stays_user_and_admin_report_is_closed():
    client.patch("/users/me", json={"role": "admin"}, headers=ALICE)
    assert mod.USERS["alice"]["role"] == "user"
    assert client.get("/admin/report", headers=ALICE).status_code == 403


def test_response_does_not_leak_api_key():
    assert "api_key" not in client.get("/users/me", headers=ALICE).json()
