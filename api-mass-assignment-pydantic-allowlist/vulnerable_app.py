"""연습용 취약 API입니다. 실제 서비스에 쓰지 마십시오.

요청 본문(JSON)을 검사 없이 사용자 기록에 합치는 구조를 일부러 만들었습니다.
인증은 X-User 헤더로 대신하는 연습용 방식입니다.
"""
from fastapi import Body, Depends, FastAPI, Header, HTTPException

app = FastAPI(title="mass-assignment vulnerable (practice only)")
USERS = {}


def seed():
    USERS.clear()
    USERS["alice"] = {"username": "alice", "display_name": "Alice", "team": "sales",
                      "role": "user", "api_key": "key-alice-111"}
    USERS["root"] = {"username": "root", "display_name": "Root", "team": "ops",
                     "role": "admin", "api_key": "key-root-999"}


seed()


def current_user(x_user: str | None = Header(default=None)):
    if x_user not in USERS:
        raise HTTPException(status_code=401, detail="X-User 헤더가 필요합니다")
    return USERS[x_user]


@app.get("/users/me")
def read_me(user: dict = Depends(current_user)):
    return user


@app.patch("/users/me")
def update_me(body: dict = Body(...), user: dict = Depends(current_user)):
    user.update(body)  # 취약: 클라이언트가 보낸 키가 그대로 기록에 들어갑니다
    return user


@app.get("/admin/report")
def admin_report(user: dict = Depends(current_user)):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="관리자만 볼 수 있습니다")
    return {"users": len(USERS), "teams": [u["team"] for u in USERS.values()]}
