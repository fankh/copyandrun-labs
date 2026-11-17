"""Ollama num_ctx 심화: 모델 두 개에서 num_ctx 별 올라간 메모리, 불러오는 시간, 속도, 그리고 입력 길이에 따른 입력 처리 시간.

준비: Ollama 설치, ollama pull exaone3.5:2.4b qwen2.5:3b-instruct-q4_K_M, pip install requests
주의: 본 서비스(11434)는 건드리지 않고 11503 포트에 임시 서버를 띄운다. 끝에서 이 서버만 끈다.
실행: python -X utf8 ctx_more.py   (약 3분)
"""
import os
import subprocess
import time

import requests

PORT = 11503
URL = f"http://127.0.0.1:{PORT}"
MODELS = ["exaone3.5:2.4b", "qwen2.5:3b-instruct-q4_K_M"]

srv = subprocess.Popen(["ollama", "serve"], env=dict(os.environ, OLLAMA_HOST=f"127.0.0.1:{PORT}", OLLAMA_KEEP_ALIVE="2m"),
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
for _ in range(30):
    try:
        requests.get(URL + "/api/version", timeout=1)
        break
    except requests.RequestException:
        time.sleep(1)


def gen(model, prompt, num_ctx, n=40):
    d = requests.post(URL + "/api/generate", json={"model": model, "prompt": prompt, "stream": False,
                      "options": {"num_ctx": num_ctx, "num_predict": n, "temperature": 0}}, timeout=900).json()
    return d


def mem(model):
    for m in requests.get(URL + "/api/ps").json()["models"]:
        if m["name"] == model:
            return m["size"] / 1e9
    return None


try:
    print("## 1. num_ctx 별 올라간 메모리(짧은 질문, /api/ps 의 크기)")
    print(f"  {'모델':<28}{'num_ctx':>8}{'메모리':>9}{'불러오기':>9}{'생성 속도':>12}")
    for m in MODELS:
        for n in (2048, 8192, 32768, 65536):
            subprocess.run(["ollama", "stop", m], env=dict(os.environ, OLLAMA_HOST=f"127.0.0.1:{PORT}"), capture_output=True)
            d = gen(m, "한 문장으로 인사해 주세요.", n)
            print(f"  {m:<28}{n:>8}{mem(m):>7.1f}GB{d['load_duration'] / 1e9:>7.1f}초{d['eval_count'] / (d['eval_duration'] / 1e9):>8.0f}tok/s")

    print("\n## 2. 입력 길이에 따른 입력 처리 시간(qwen2.5:3b, num_ctx 8192)")
    m = MODELS[1]
    sentence = "서버의 디스크 사용률은 높고 점검자는 김씨입니다. "
    print(f"  {'넣은 글자 수':>10}{'읽은 토큰':>10}{'입력 처리 시간':>14}{'토큰/초':>10}")
    gen(m, "준비", 8192, 1)
    for reps in (20, 80, 320):
        d = gen(m, sentence * reps + "\n위 내용을 한 단어로 요약하세요.", 8192, 5)
        pe, pd = d["prompt_eval_count"], d["prompt_eval_duration"] / 1e9
        print(f"  {len(sentence) * reps:>10}{pe:>10}{pd:>12.2f}초{pe / pd:>10.0f}")
finally:
    srv.terminate()
    srv.wait(timeout=30)
    time.sleep(1)
    r = subprocess.run(["netstat", "-ano"], capture_output=True, text=True).stdout
    print("\n## 3. 정리: 임시 서버 11503 포트가 열린 줄 수:", sum(1 for l in r.splitlines() if f":{PORT} " in l and "LISTENING" in l))
