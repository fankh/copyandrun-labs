"""Authorization Code + PKCE 로 Keycloak 에 로그인하는 작은 Flask 클라이언트.

실행: CLIENT_ID=lab-pkce python app.py  (기본값 lab-pkce)
"""
import base64
import hashlib
import html
import json
import os
import secrets
import time
from urllib.parse import urlencode

import jwt
import requests
from flask import Flask, redirect, request, session

ISSUER = os.environ.get("ISSUER", "http://localhost:5480/realms/lab")
CLIENT_ID = os.environ.get("CLIENT_ID", "lab-pkce")
REDIRECT_URI = "http://localhost:5481/callback"

app = Flask(__name__)
app.secret_key = "lab-only-session-key"  # 실습용 값입니다. 실제 서비스에서는 무작위 비밀값을 환경 변수로 받습니다.

PAGE = """<!doctype html><meta charset="utf-8"><title>OIDC 클라이언트</title>
<style>
body{{font-family:'Malgun Gothic',sans-serif;margin:32px;color:#222}}
table{{border-collapse:collapse;min-width:760px}}
th,td{{border:1px solid #ccc;padding:8px 14px;text-align:left}}
th{{background:#f2f4f7}} .ok{{background:#dff5e1;color:#14692a;font-weight:700}}
.bad{{background:#fde1e1;color:#a11919;font-weight:700}} code{{font-size:13px}}
a.btn{{display:inline-block;padding:10px 22px;background:#1a5fb4;color:#fff;text-decoration:none;border-radius:4px}}
</style>{body}"""


def b64url(raw):
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode()


def discovery():
    return requests.get(f"{ISSUER}/.well-known/openid-configuration", timeout=5).json()


@app.get("/")
def index():
    body = (f"<h1>OIDC 클라이언트</h1><p>client_id: <code>{html.escape(CLIENT_ID)}</code> / "
            f"issuer: <code>{html.escape(ISSUER)}</code></p>"
            '<p><a class="btn" href="/login">Keycloak 으로 로그인</a></p>')
    return PAGE.format(body=body)


@app.get("/login")
def login():
    verifier = b64url(secrets.token_bytes(32))
    challenge = b64url(hashlib.sha256(verifier.encode()).digest())
    session["verifier"] = verifier
    session["state"] = secrets.token_urlsafe(16)
    session["nonce"] = secrets.token_urlsafe(16)
    query = urlencode({
        "client_id": CLIENT_ID, "response_type": "code", "scope": "openid profile",
        "redirect_uri": REDIRECT_URI, "state": session["state"], "nonce": session["nonce"],
        "code_challenge": challenge, "code_challenge_method": "S256",
    })
    return redirect(discovery()["authorization_endpoint"] + "?" + query)


@app.get("/callback")
def callback():
    if request.args.get("state") != session.get("state"):
        return PAGE.format(body="<h1>state 가 맞지 않습니다</h1>"), 400
    if "code" not in request.args:
        return PAGE.format(body=f"<h1>인증 실패</h1><p>{html.escape(request.args.get('error_description', '-'))}</p>"), 400
    conf = discovery()
    resp = requests.post(conf["token_endpoint"], data={
        "grant_type": "authorization_code", "code": request.args["code"],
        "redirect_uri": REDIRECT_URI, "client_id": CLIENT_ID,
        "code_verifier": session["verifier"],
    }, timeout=5)
    if resp.status_code != 200:
        return PAGE.format(body=f"<h1>토큰 교환 실패</h1><pre>{html.escape(resp.text)}</pre>"), 400
    id_token = resp.json()["id_token"]
    key = jwt.PyJWKClient(conf["jwks_uri"]).get_signing_key_from_jwt(id_token).key
    claims = jwt.decode(id_token, key, algorithms=["RS256"], audience=CLIENT_ID, issuer=ISSUER)
    checks = [
        ("iss", claims["iss"], claims["iss"] == ISSUER, f"기대값 {ISSUER}"),
        ("aud", claims["aud"], claims["aud"] == CLIENT_ID, f"기대값 {CLIENT_ID}"),
        ("exp", time.strftime("%H:%M:%S", time.localtime(claims["exp"])),
         claims["exp"] > time.time(), "지금보다 뒤"),
        ("nonce", claims.get("nonce"), claims.get("nonce") == session["nonce"], "로그인 시작 때 보낸 값과 같음"),
    ]
    rows = "".join(
        f"<tr><td>{n}</td><td><code>{html.escape(str(v))}</code></td>"
        f"<td class='{'ok' if ok else 'bad'}'>{'통과' if ok else '실패'}</td><td>{html.escape(why)}</td></tr>"
        for n, v, ok, why in checks)
    body = (f"<h1>로그인 성공: {html.escape(claims.get('preferred_username', '-'))}</h1>"
            f"<h3>ID 토큰 검증</h3><table><tr><th>클레임</th><th>값</th><th>결과</th><th>기준</th></tr>{rows}</table>"
            f"<h3>전체 클레임</h3><pre>{html.escape(json.dumps(claims, indent=2, ensure_ascii=False))}</pre>")
    return PAGE.format(body=body)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5481)
