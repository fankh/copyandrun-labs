"""같은 한국어 질문 다섯 개를 크기가 다른 모델 네 개에 보내 속도와 답을 저장한다.

준비: Ollama 실행 중, 아래 MODELS 를 ollama pull 로 받아 둔다, pip install requests
주의: 큰 모델(17GB, 20GB)을 메모리에 올리므로 다른 큰 모델이 떠 있으면 느려진다. 약 3~5분.
실행: python -X utf8 compare_models.py   (답 전체는 answers.json 에 저장된다)
"""
import json
import re
import time

import requests

URL = "http://localhost:11434/api/chat"
MODELS = ["exaone3.5:2.4b", "qwen2.5:3b-instruct-q4_K_M", "qwen3.8:27b", "gemma4:31b"]
QS = [
    "'회식'과 '회의'의 차이를 한 문장씩 설명해 주세요.",
    "\"내일 회의 못 가요\"를 정중한 존댓말 이메일 문장으로 바꿔 주세요.",
    "사과 3개에서 2개를 먹고 5개를 더 샀습니다. 숫자만 답하세요.",
    "'방화벽'을 초등학생에게 두 문장으로 설명해 주세요.",
    "파이썬으로 리스트의 중복을 제거하는 한 줄 코드를 보여 주세요.",
]


def ask(model, q):
    body = {"model": model, "stream": False, "think": False,
            "options": {"temperature": 0.2, "num_predict": 300},
            "messages": [{"role": "user", "content": q}]}
    r = requests.post(URL, json=body, timeout=900)
    if r.status_code != 200:                # think 옵션을 못 받는 모델은 옵션 없이 다시 보낸다
        body.pop("think")
        r = requests.post(URL, json=body, timeout=900)
    return r.json()


def sentences(text):
    return len([s for s in re.split(r"(?<=[.?!])\s+", text.strip()) if s])


answers = {}
speed = {}
for m in MODELS:
    answers[m] = []
    rates = []
    for q in QS:
        d = ask(m, q)
        text = d["message"]["content"].strip()
        answers[m].append(text)
        rates.append(d["eval_count"] / (d["eval_duration"] / 1e9))
    speed[m] = sum(rates) / len(rates)
    print(f"{m} 완료", flush=True)

print("\n## 1. 평균 생성 속도(질문 다섯 개의 평균)")
for m in MODELS:
    print(f"{m:<28} {speed[m]:6.1f} 토큰/초")

print("\n## 2. 3번 사과 문제(정답 6)")
for m in MODELS:
    a = answers[m][2]
    print(f"{m:<28} {a[:20]!r:<24} {'맞음' if a.strip().rstrip('.') == '6' else '틀림'}")

print("\n## 3. 4번 방화벽: 두 문장 지시를 지켰나(문장 수)")
for m in MODELS:
    n = sentences(answers[m][3])
    print(f"{m:<28} {n}문장 {'지킴' if n == 2 else '어김'}")

with open("answers.json", "w", encoding="utf-8") as f:
    json.dump(answers, f, ensure_ascii=False, indent=1)
print("\n답 전체를 answers.json 에 저장했습니다.")
