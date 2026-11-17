"""Ollama keep_alive 심화: 값의 여러 표기, 서비스 기본값(OLLAMA_KEEP_ALIVE)과 요청값의 우선순위, 모델 크기별 첫 호출 비용.

준비: Ollama 설치, ollama pull exaone3.5:2.4b qwen2.5:3b-instruct-q4_K_M gemma4:31b, pip install requests
주의: 본 서비스(11434)는 건드리지 않고, 11501 포트에 임시 서버를 따로 띄운다(OLLAMA_KEEP_ALIVE=10s). 끝에서 이 서버만 끈다.
      큰 모델(20GB)을 임시 서버가 한 번 더 올리므로 메모리가 넉넉한 PC에서만 실행한다.
실행: python -X utf8 keep_alive_more.py   (약 3분)
"""
import os
import subprocess
import time
from datetime import datetime, timezone

import requests

PORT = 11501
URL = f"http://127.0.0.1:{PORT}"
SMALL, MID, BIG = "exaone3.5:2.4b", "qwen2.5:3b-instruct-q4_K_M", "gemma4:31b"

env = dict(os.environ, OLLAMA_HOST=f"127.0.0.1:{PORT}", OLLAMA_KEEP_ALIVE="10s")
srv = subprocess.Popen(["ollama", "serve"], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
for _ in range(30):
    try:
        requests.get(URL + "/api/version", timeout=1)
        break
    except requests.RequestException:
        time.sleep(1)


def gen(model, keep=None, n=5):
    body = {"model": model, "prompt": "안녕", "stream": False, "options": {"num_predict": n}}
    if keep is not None:
        body["keep_alive"] = keep
    t = time.time()
    d = requests.post(URL + "/api/generate", json=body, timeout=600).json()
    if "error" in d:
        return d["error"], None
    return d["load_duration"] / 1e9, time.time() - t


def remaining(model):
    """/api/ps 의 expires_at 에서 지금까지 남은 초(없으면 None)"""
    for m in requests.get(URL + "/api/ps").json()["models"]:
        if m["name"] == model:
            e = datetime.fromisoformat(m["expires_at"].replace("Z", "+00:00"))
            return (e - datetime.now(timezone.utc)).total_seconds()
    return None


def fmt(s):
    return "메모리에 없음" if s is None else ("무기한" if s > 3e8 else f"약 {s:.0f}초 뒤 내려감")


try:
    print("## 1. keep_alive 표기별로 모델이 얼마나 남는가(exaone, 호출 직후 /api/ps 의 expires_at)")
    for keep in (0, "0", 30, "30s", "2m", "1h", -1, "-1", None):
        subprocess.run(["ollama", "stop", SMALL], env=env, capture_output=True)
        err, _ = gen(SMALL, keep)
        label = "(지정 안 함, 서버 기본값 10s)" if keep is None else repr(keep)
        print(f"  keep_alive={label:<30} -> {('오류: ' + str(err)[:70]) if isinstance(err, str) else fmt(remaining(SMALL))}")

    print("\n## 2. 서버 기본값(10s)이 실제로 지켜지는가: 지정 없이 호출한 뒤 5초, 15초 후")
    subprocess.run(["ollama", "stop", SMALL], env=env, capture_output=True)
    gen(SMALL)
    time.sleep(5)
    a = remaining(SMALL)
    time.sleep(10)
    b = remaining(SMALL)
    print(f"  호출 5초 뒤: {fmt(a)}   /   15초 뒤: {fmt(b)}")

    print("\n## 3. 요청의 keep_alive 가 서버 기본값보다 우선하는가: keep_alive=\"1m\" 로 호출하고 15초 뒤")
    gen(SMALL, "1m")
    time.sleep(15)
    print(f"  15초 뒤: {fmt(remaining(SMALL))}")

    print("\n## 4. 첫 호출(모델 불러오기) 비용과 이어서 부른 비용 - 모델 크기별")
    print(f"  {'모델':<28}{'첫 호출 불러오기':>16}{'첫 호출 전체':>12}{'이어서 부른 전체':>16}")
    for m in (SMALL, MID, BIG):
        subprocess.run(["ollama", "stop", m], env=env, capture_output=True)
        l1, t1 = gen(m, "1m")
        l2, t2 = gen(m, "1m")
        print(f"  {m:<28}{l1:>14.1f}초{t1:>10.1f}초{t2:>14.1f}초")
        subprocess.run(["ollama", "stop", m], env=env, capture_output=True)
finally:
    srv.terminate()
    srv.wait(timeout=30)
    time.sleep(1)
    r = subprocess.run(["netstat", "-ano"], capture_output=True, text=True).stdout
    print("\n## 5. 정리: 임시 서버 11501 포트가 열린 줄 수:", sum(1 for l in r.splitlines() if f":{PORT} " in l and "LISTENING" in l))
