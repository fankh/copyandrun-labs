"""vulnerable_app.py의 수정판입니다. 연습용이며 실제 서비스에 쓰지 마십시오.

엔드포인트마다 응답 모델을 따로 두고 response_model로 지정해, 모델에 없는 필드는 응답에서 걸러 냅니다.
"""
from fastapi import Depends, FastAPI, Header, HTTPException
from pydantic import BaseModel

from vulnerable_app import USERS  # 같은 가짜 데이터를 씁니다

app = FastAPI(title="excessive-data-exposure fixed (practice only)")


class PublicUser(BaseModel):
    """다른 사용자에게 보여 줄 필드만 선언합니다."""
    username: str
    display_name: str
    team: str


class MyProfile(PublicUser):
    """본인에게만 보여 주는 필드를 더합니다. 해시와 내부 메모는 여기에도 넣지 않습니다."""
    email: str
    phone: str
    role: str


def current_user(x_user: str | None = Header(default=None)):
    if x_user not in USERS:
        raise HTTPException(status_code=401, detail="X-User 헤더가 필요합니다")
    return USERS[x_user]


@app.get("/users/me", response_model=MyProfile)
def read_me(user: dict = Depends(current_user)):
    return user


@app.get("/users/{username}", response_model=PublicUser)
def read_user(username: str, user: dict = Depends(current_user)):
    if username not in USERS:
        raise HTTPException(status_code=404, detail="없는 사용자입니다")
    return USERS[username]


@app.get("/users", response_model=list[PublicUser])
def list_users(user: dict = Depends(current_user)):
    return list(USERS.values())
