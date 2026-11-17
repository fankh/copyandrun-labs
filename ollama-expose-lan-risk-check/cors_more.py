"""Ollama 의 웹 접근 제어 심화: 브라우저가 보내는 Origin 헤더, Host 헤더, OLLAMA_ORIGINS 설정이 응답을 어떻게 바꾸는가.

준비: Ollama 설치, pip install requests
주의: 본 서비스(11434)는 건드리지 않고 11504 포트에 임시 서버를 설정마다 새로 띄운다. 끝에서 이 서버만 끈다.
      이 시험은 같은 PC 안(127.0.0.1)에서 헤더만 바꿔 보낸다. 다른 기기에서 접속한 것이 아니다.
실행: python -X utf8 cors_more.py   (약 40초)
"""
import os
import subprocess
import time

import requests

PORT = 11504
URL = f"http://127.0.0.1:{PORT}/api/tags"


def start(extra):
    env = dict(os.environ, OLLAMA_HOST=f"127.0.0.1:{PORT}", **extra)
    env.pop("OLLAMA_ORIGINS", None) if "OLLAMA_ORIGINS" not in extra else None
    p = subprocess.Popen(["ollama", "serve"], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(30):
        try:
            requests.get(URL, timeout=1)
            break
        except requests.RequestException:
            time.sleep(1)
    return p


def get(headers=None, method="GET"):
    r = requests.request(method, URL, headers=headers or {}, timeout=10)
    return r.status_code, r.headers.get("Access-Control-Allow-Origin", "-")


CASES = [
    ("헤더 없음(curl 같은 도구)", {}),
    ("Origin: http://localhost:3000", {"Origin": "http://localhost:3000"}),
    ("Origin: http://127.0.0.1:5173", {"Origin": "http://127.0.0.1:5173"}),
    ("Origin: https://evil.example", {"Origin": "https://evil.example"}),
    ("Origin: https://my.app", {"Origin": "https://my.app"}),
    ("Host: evil.example", {"Host": "evil.example"}),
]

for title, extra in (("기본 설정", {}), ("OLLAMA_ORIGINS=https://my.app", {"OLLAMA_ORIGINS": "https://my.app"})):
    srv = start(extra)
    try:
        print(f"## {title}")
        print(f"  {'보낸 헤더':<34}{'응답 코드':>8}  Access-Control-Allow-Origin")
        for label, h in CASES:
            code, allow = get(h)
            print(f"  {label:<34}{code:>8}  {allow}")
        code, allow = get({"Origin": "https://evil.example", "Access-Control-Request-Method": "GET"}, "OPTIONS")
        print(f"  {'사전 확인(OPTIONS), evil Origin':<34}{code:>8}  {allow}")
    finally:
        srv.terminate()
        srv.wait(timeout=30)
        time.sleep(2)
    print()

r = subprocess.run(["netstat", "-ano"], capture_output=True, text=True).stdout
print("정리: 임시 서버 11504 포트가 열린 줄 수:", sum(1 for l in r.splitlines() if f":{PORT} " in l and "LISTENING" in l))
