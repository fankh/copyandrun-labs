"""시험용 키 두 쌍을 만들고, 정상 토큰 하나와 공격 토큰 여섯 개를 tokens.json 으로 저장한다.
사용: python make_tokens.py 출력폴더"""
import base64
import hashlib
import hmac
import json
import sys
import time

import jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

out = sys.argv[1]
ISS, AUD = "https://auth.lab", "shop-api"


def new_key():
    return rsa.generate_private_key(public_exponent=65537, key_size=2048)


def pem_priv(k):
    return k.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8, serialization.NoEncryption())


def pem_pub(k):
    return k.public_key().public_bytes(serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo)


def b64(data):
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


server, attacker = new_key(), new_key()
now = int(time.time())
user = {"sub": "alice", "role": "user", "iss": ISS, "aud": AUD, "iat": now, "exp": now + 600}
admin = dict(user, sub="mallory", role="admin")

good = jwt.encode(user, pem_priv(server), algorithm="RS256")

# 1) 서명이 없는 토큰(alg none)
none_tok = b64(json.dumps({"alg": "none", "typ": "JWT"}).encode()) + "." + b64(json.dumps(admin).encode()) + "."
# 2) 공격자 키로 서명한 토큰
wrong_key = jwt.encode(admin, pem_priv(attacker), algorithm="RS256")
# 3) 만료된 토큰(서명은 진짜)
expired = jwt.encode(dict(user, iat=now - 7200, exp=now - 3600), pem_priv(server), algorithm="RS256")
# 4) 다른 서비스용 토큰(서명은 진짜, aud 만 다름)
wrong_aud = jwt.encode(dict(user, aud="billing-api"), pem_priv(server), algorithm="RS256")
# 5) 본문만 바꾼 토큰(서명은 그대로)
h, p, s = good.split(".")
tampered = h + "." + b64(json.dumps(admin).encode()) + "." + s
# 6) 알고리즘 혼동: 공개키 PEM 을 HMAC 비밀로 써서 HS256 으로 직접 서명(PyJWT 의 보호를 피해 손으로 만듦)
head = b64(json.dumps({"alg": "HS256", "typ": "JWT"}).encode()) + "." + b64(json.dumps(admin).encode())
sig = hmac.new(pem_pub(server), head.encode(), hashlib.sha256).digest()
confusion = head + "." + b64(sig)

tokens = {"정상 토큰": good, "alg none": none_tok, "다른 키 서명": wrong_key, "만료": expired,
          "다른 aud": wrong_aud, "본문 변조": tampered, "HS256 혼동": confusion}
json.dump(tokens, open(f"{out}/tokens.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
open(f"{out}/server_pub.pem", "wb").write(pem_pub(server))
print(f"토큰 {len(tokens)}개와 공개키를 {out} 에 저장")
