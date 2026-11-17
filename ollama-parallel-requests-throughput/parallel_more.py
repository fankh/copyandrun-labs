"""Ollama 동시 요청 심화: OLLAMA_NUM_PARALLEL 을 1, 4 로 바꾼 임시 서버에서 같은 시험을 해 처리량과 대기를 비교한다.

준비: Ollama 설치, ollama pull exaone3.5:2.4b, pip install requests
주의: 본 서비스(11434)는 건드리지 않고 11502 포트에 임시 서버를 설정마다 새로 띄운다. 끝에서 이 서버만 끈다.
실행: python -X utf8 parallel_more.py   (약 2분)
"""
import os
import subprocess
import threading
import time

import requests

PORT = 11502
URL = f"http://127.0.0.1:{PORT}/api/chat"
MODEL = "exaone3.5:2.4b"
Q = "로컬 AI를 쓰는 이유를 세 가지 말해 주세요."


def start(parallel):
    env = dict(os.environ, OLLAMA_HOST=f"127.0.0.1:{PORT}", OLLAMA_NUM_PARALLEL=str(parallel), OLLAMA_KEEP_ALIVE="5m")
    p = subprocess.Popen(["ollama", "serve"], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(30):
        try:
            requests.get(f"http://127.0.0.1:{PORT}/api/version", timeout=1)
            break
        except requests.RequestException:
            time.sleep(1)
    return p


def one(res, i):
    t = time.time()
    d = requests.post(URL, json={"model": MODEL, "stream": False, "messages": [{"role": "user", "content": Q}],
                                 "options": {"temperature": 0.2, "num_predict": 150}}, timeout=600).json()
    res[i] = (d["eval_count"], time.time() - t)


def ctx_and_mem():
    for m in requests.get(f"http://127.0.0.1:{PORT}/api/ps").json()["models"]:
        return m.get("context_length"), m["size"] / 1e9
    return None, None


print("설정                 동시 요청 | 전체 시간 | 전체 처리량 | 요청당 평균 대기 | 가장 늦게 끝난 요청")
for parallel in (1, 4):
    srv = start(parallel)
    try:
        requests.post(URL, json={"model": MODEL, "stream": False, "messages": [{"role": "user", "content": "hi"}],
                                 "options": {"num_predict": 2}})     # 모델을 먼저 올려 둔다
        for n in (1, 4, 8):
            res = [None] * n
            ths = [threading.Thread(target=one, args=(res, i)) for i in range(n)]
            t = time.time()
            [x.start() for x in ths]
            [x.join() for x in ths]
            wall = time.time() - t
            tot = sum(r[0] for r in res)
            print(f"NUM_PARALLEL={parallel:<2}{n:>10} | {wall:7.1f}초 | {tot / wall:6.0f} tok/s | "
                  f"{sum(r[1] for r in res) / n:10.1f}초 | {max(r[1] for r in res):8.1f}초")
        c, g = ctx_and_mem()
        print(f"  (NUM_PARALLEL={parallel}일 때 올라간 모델: 컨텍스트 {c}, 메모리 {g:.1f}GB)")
    finally:
        srv.terminate()
        srv.wait(timeout=30)
        time.sleep(2)

r = subprocess.run(["netstat", "-ano"], capture_output=True, text=True).stdout
print("정리: 임시 서버 11502 포트가 열린 줄 수:", sum(1 for l in r.splitlines() if f":{PORT} " in l and "LISTENING" in l))
