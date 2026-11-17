"""vulnerable_app.py의 수정판입니다. 연습용이며 실제 서비스에 쓰지 마십시오.

입력 모델은 허용 필드만 받고(extra="forbid"), 응답은 별도 출력 모델로 걸러 냅니다.
"""
from fastapi import Depends, FastAPI, Header, HTTPException
from pydantic import BaseModel, ConfigDict, Field

app = FastAPI(title="mass-assignment fixed (practice only)")
USERS = {}


def seed():
    USERS.clear()
    USERS["alice"] = {"username": "alice", "display_name": "Alice", "team": "sales",
                      "role": "user", "api_key": "key-alice-111"}
    USERS["root"] = {"username": "root", "display_name": "Root", "team": "ops",
                     "role": "admin", "api_key": "key-root-999"}


seed()


class ProfileUpdate(BaseModel):
    """클라이언트가 바꿀 수 있는 필드만 선언합니다."""
    model_config = ConfigDict(extra="forbid")
    # str 로 선언해 null 을 거절합니다. 기본값은 exclude_unset 때문에 쓰이지 않습니다
    display_name: str = Field(default="", min_length=1, max_length=40)
    team: str = Field(default="", min_length=1, max_length=40)


class UserOut(BaseModel):
    """응답에 담을 필드만 선언합니다. api_key는 넣지 않습니다."""
    username: str
    display_name: str
    team: str
    role: str


def current_user(x_user: str | None = Header(default=None)):
    if x_user not in USERS:
        raise HTTPException(status_code=401, detail="X-User 헤더가 필요합니다")
    return USERS[x_user]


@app.get("/users/me", response_model=UserOut)
def read_me(user: dict = Depends(current_user)):
    return user


@app.patch("/users/me", response_model=UserOut)
def update_me(body: ProfileUpdate, user: dict = Depends(current_user)):
    user.update(body.model_dump(exclude_unset=True))
    return user


@app.get("/admin/report")
def admin_report(user: dict = Depends(current_user)):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="관리자만 볼 수 있습니다")
    return {"users": len(USERS), "teams": [u["team"] for u in USERS.values()]}
