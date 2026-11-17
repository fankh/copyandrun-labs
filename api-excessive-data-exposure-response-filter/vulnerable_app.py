"""연습용 취약 API입니다. 실제 서비스에 쓰지 마십시오.

저장된 사용자 기록(딕셔너리)을 걸러 내지 않고 그대로 반환하는 구조를 일부러 만들었습니다.
인증은 X-User 헤더로 대신하는 연습용 방식이고, 데이터는 모두 가짜입니다.
"""
from fastapi import Depends, FastAPI, Header, HTTPException

app = FastAPI(title="excessive-data-exposure vulnerable (practice only)")

DOMAIN = "example.com"  # 예약된 예시 도메인만 씁니다

USERS = {
    "alice": {"id": 1, "internal_id": "emp-00417", "username": "alice",
              "display_name": "Alice", "email": f"alice@{DOMAIN}",
              "phone": "010-0000-1111", "team": "sales", "role": "user",
              "password_hash": "pbkdf2$fake$9f2c41aa7d", "internal_note": "VIP 계약 갱신 예정"},
    "dana": {"id": 2, "internal_id": "emp-00532", "username": "dana",
             "display_name": "Dana", "email": f"dana@{DOMAIN}",
             "phone": "010-0000-2222", "team": "ops", "role": "user",
             "password_hash": "pbkdf2$fake$3b7d90c1e5", "internal_note": "결제 지연 이력 있음"},
    "root": {"id": 3, "internal_id": "emp-00001", "username": "root",
             "display_name": "Root", "email": f"root@{DOMAIN}",
             "phone": "010-0000-3333", "team": "ops", "role": "admin",
             "password_hash": "pbkdf2$fake$c04e8a6b12", "internal_note": "관리자 계정"},
}


def current_user(x_user: str | None = Header(default=None)):
    if x_user not in USERS:
        raise HTTPException(status_code=401, detail="X-User 헤더가 필요합니다")
    return USERS[x_user]


@app.get("/users/me")
def read_me(user: dict = Depends(current_user)):
    return user  # 취약: 기록 전체가 응답으로 나갑니다


@app.get("/users/{username}")
def read_user(username: str, user: dict = Depends(current_user)):
    if username not in USERS:
        raise HTTPException(status_code=404, detail="없는 사용자입니다")
    return USERS[username]  # 취약: 다른 사용자의 개인정보와 내부 값까지 나갑니다


@app.get("/users")
def list_users(user: dict = Depends(current_user)):
    return list(USERS.values())  # 취약: 목록 전체가 그대로 나갑니다
