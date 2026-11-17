"""Vaultwarden 을 도커로 띄워 가입 차단, 계정 만들기와 로그인, 정지 후 백업, 복원 뒤 로그인, 키 파일 없이 복원까지 확인한다.

준비: Docker, pip install requests cryptography
주의: osk-vw 컨테이너와 osk_vw, osk_vw_bk 볼륨을 만들고 끝에서 지운다. 같은 이름이 있으면 먼저 지운다.
      127.0.0.1:3902 에만 열고, 만드는 계정은 실습용(lab@example.com)이다. 실제 비밀번호를 넣지 않는다.
실행: python -X utf8 vw_test.py   (약 1분)
"""
import base64
import hashlib
import hmac
import os
import subprocess
import time
import uuid

import requests
from cryptography.hazmat.primitives import padding, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

PORT = 3902
URL = f"http://127.0.0.1:{PORT}"
NAME, VOL, BK = "osk-vw", "osk_vw", "osk_vw_bk"
IMAGE = "vaultwarden/server:1.37.4"
EMAIL, PW, ITER = "lab@example.com", "Lab-Only-Pass-1", 100000


def sh(*a, check=True):
    r = subprocess.run(a, capture_output=True, text=True)
    if check and r.returncode:
        raise RuntimeError(f"{a}: {r.stderr.strip()}")
    return r.stdout.strip()


def cleanup():
    sh("docker", "rm", "-f", NAME, check=False)
    sh("docker", "volume", "rm", VOL, BK, check=False)


def start(signups):
    sh("docker", "rm", "-f", NAME, check=False)
    sh("docker", "run", "-d", "--name", NAME, "-p", f"127.0.0.1:{PORT}:80", "-v", f"{VOL}:/data",
       "-e", f"SIGNUPS_ALLOWED={signups}", IMAGE)
    for _ in range(60):
        try:
            if requests.get(URL + "/alive", timeout=2).status_code == 200:
                return
        except requests.RequestException:
            pass
        time.sleep(1)
    raise RuntimeError("Vaultwarden 이 시작되지 않았다")


def b64(b):
    return base64.b64encode(b).decode()


def hkdf_expand(key, info):
    return hmac.new(key, info + b"\x01", hashlib.sha256).digest()


def enc_string(enc_key, mac_key, data):
    """Bitwarden 의 '2.iv|암호문|mac' 형식(AES-256-CBC + HMAC-SHA256)으로 암호화한다."""
    iv = os.urandom(16)
    padder = padding.PKCS7(128).padder()
    c = Cipher(algorithms.AES(enc_key), modes.CBC(iv)).encryptor()
    ct = c.update(padder.update(data) + padder.finalize()) + c.finalize()
    return f"2.{b64(iv)}|{b64(ct)}|{b64(hmac.new(mac_key, iv + ct, hashlib.sha256).digest())}"


def pw_hash():
    master = hashlib.pbkdf2_hmac("sha256", PW.encode(), EMAIL.encode(), ITER, 32)
    return master, b64(hashlib.pbkdf2_hmac("sha256", master, PW.encode(), 1, 32))


def register():
    """가입 3단계: 이메일 확인 토큰 받기(메일을 쓰지 않으면 응답에 토큰이 들어 있다) -> 키 만들기 -> 가입 완료."""
    r = requests.post(URL + "/identity/accounts/register/send-verification-email",
                      json={"email": EMAIL, "name": "lab", "receiveMarketingEmails": False}, timeout=20)
    if r.status_code != 200:
        return r
    token = r.text.strip('"')
    master, h = pw_hash()
    stretched_enc, stretched_mac = hkdf_expand(master, b"enc"), hkdf_expand(master, b"mac")
    user_key = os.urandom(64)
    priv = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    pub_der = priv.public_key().public_bytes(serialization.Encoding.DER, serialization.PublicFormat.SubjectPublicKeyInfo)
    priv_der = priv.private_bytes(serialization.Encoding.DER, serialization.PrivateFormat.PKCS8, serialization.NoEncryption())
    return requests.post(URL + "/identity/accounts/register/finish", json={
        "email": EMAIL, "emailVerificationToken": token, "masterPasswordHash": h, "masterPasswordHint": "",
        "userSymmetricKey": enc_string(stretched_enc, stretched_mac, user_key),
        "userAsymmetricKeys": {"publicKey": b64(pub_der),
                               "encryptedPrivateKey": enc_string(user_key[:32], user_key[32:], priv_der)},
        "kdf": 0, "kdfIterations": ITER}, timeout=30)


def login():
    _, h = pw_hash()
    return requests.post(URL + "/identity/connect/token", data={
        "grant_type": "password", "username": EMAIL, "password": h, "scope": "api offline_access",
        "client_id": "web", "deviceType": 9, "deviceIdentifier": str(uuid.uuid4()), "deviceName": "lab"}, timeout=20)


def users():
    out = sh("docker", "run", "--rm", "-v", f"{VOL}:/data", "alpine", "sh", "-c", "ls -l /data | tr -s ' ' | cut -d' ' -f5,9")
    return out.replace("\n", " | ")


cleanup()
print("## 1. SIGNUPS_ALLOWED=false 로 띄우고 가입 시도")
start("false")
r = register()
print("가입 응답:", r.status_code, r.text[:90].replace("\n", " "))

print("## 2. SIGNUPS_ALLOWED=true 로 다시 띄워 계정 하나 만들고 로그인")
start("true")
r = register()
print("가입 응답:", r.status_code)
r = login()
print("로그인 응답:", r.status_code, "access_token 받음:", "access_token" in r.json())
print("/data 내용(크기 | 이름):", users())

print("## 3. 정지 후 백업(세 가지: 볼륨 전체 / 키 파일만 뺀 것 / db.sqlite3 한 개)")
sh("docker", "stop", NAME)
sh("docker", "run", "--rm", "-v", f"{VOL}:/data", "-v", f"{BK}:/bk", "alpine", "sh", "-c",
   "mkdir -p /bk/full /bk/nokey /bk/dbfile && cp -a /data/. /bk/full/ && cp /data/db.sqlite3* /bk/nokey/ && cp /data/db.sqlite3 /bk/dbfile/")
for d in ("full", "nokey", "dbfile"):
    print(f"{d:<7}:", sh("docker", "run", "--rm", "-v", f"{BK}:/bk", "alpine", "ls", f"/bk/{d}").replace("\n", " "))


def restore(d):
    sh("docker", "rm", "-f", NAME)
    sh("docker", "volume", "rm", VOL)
    sh("docker", "run", "--rm", "-v", f"{VOL}:/data", "-v", f"{BK}:/bk", "alpine", "sh", "-c", f"cp -a /bk/{d}/. /data/")
    start("false")
    r = login()
    return r.status_code, "access_token" in r.json()


print("## 4. 원본을 지우고 전체 백업으로 복원 -> 같은 계정으로 로그인")
print("전체 복원 뒤 로그인:", restore("full"))
print("## 5. 원본을 지우고 키 파일(rsa_key.pem)만 뺀 백업으로 복원 -> 로그인")
print("키 파일 없이 복원 뒤 로그인:", restore("nokey"))
print("새로 만들어진 /data(크기 | 이름):", users())
print("## 6. 원본을 지우고 db.sqlite3 한 개만으로 복원 -> 로그인")
print("db.sqlite3 한 개만 복원 뒤 로그인:", restore("dbfile"))

print("## 7. 정리")
cleanup()
print("남은 osk-vw 컨테이너:", len(sh("docker", "ps", "-a", "--filter", f"name={NAME}", "--format", "{{.Names}}").split()))
