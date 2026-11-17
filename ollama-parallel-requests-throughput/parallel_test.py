"""Ollama 동시 요청: 같은 질문을 1, 2, 4, 8, 16개 동시에 보내 전체 처리량과 요청별 속도를 잰다.

준비: Ollama 실행 중, ollama pull exaone3.5:2.4b, pip install requests
주의: 서버 설정(OLLAMA_NUM_PARALLEL)은 바꾸지 않는다. 이 PC의 기본 동작을 그대로 잰다.
실행: python -X utf8 parallel_test.py   (약 1분)
"""
import threading
import time
import requests

URL = "http://localhost:11434/api/chat"
MODEL = "exaone3.5:2.4b"
Q = "로컬 AI를 쓰는 이유를 세 가지 말해 주세요."


def one(res, i):
    t = time.time()
    d = requests.post(URL, json={"model": MODEL, "stream": False,
                                 "messages": [{"role": "user", "content": Q}],
                                 "options": {"temperature": 0.2, "num_predict": 150}}, timeout=600).json()
    # (생성 토큰 수, 이 요청이 끝날 때까지 걸린 초, 이 요청의 생성 속도)
    res[i] = (d["eval_count"], time.time() - t, d["eval_count"] / (d["eval_duration"] / 1e9))


# 모델을 먼저 올려 두어 불러오는 시간이 결과에 섞이지 않게 한다
requests.post(URL, json={"model": MODEL, "stream": False,
                         "messages": [{"role": "user", "content": "hi"}], "options": {"num_predict": 2}})

print("동시 요청 | 전체 시간 | 생성 토큰 합 | 전체 처리량 | 요청별 속도 | 요청별 대기")
for n in (1, 2, 4, 8, 16):
    res = [None] * n
    ths = [threading.Thread(target=one, args=(res, i)) for i in range(n)]
    t = time.time()
    [x.start() for x in ths]
    [x.join() for x in ths]
    wall = time.time() - t
    tot = sum(r[0] for r in res)
    print(f"{n:9d} | {wall:7.1f}초 | {tot:11d} | {tot / wall:6.0f} tok/s | "
          f"{sum(r[2] for r in res) / n:6.0f} tok/s | {sum(r[1] for r in res) / n:6.1f}초")
