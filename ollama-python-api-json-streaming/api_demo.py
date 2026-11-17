"""Ollama HTTP API 를 requests 로 부른다: 한 번에 받기, 옵션 넘기기, JSON 형식 고정, 스트리밍.

준비: Ollama 실행 중, ollama pull exaone3.5:2.4b, pip install requests
실행: python -X utf8 api_demo.py   (약 40초)
"""
import json
import time

import requests

URL = "http://localhost:11434"
MODEL = "exaone3.5:2.4b"


def chat(prompt, **kw):
    r = requests.post(f"{URL}/api/chat", json={
        "model": MODEL, "stream": False,
        "messages": [{"role": "user", "content": prompt}], **kw}, timeout=300)
    r.raise_for_status()
    return r.json()


print("## 1. 한 번에 받기")
d = chat("회사 노트북 비밀번호를 잊어버렸습니다. 어떻게 해야 하나요?", options={"seed": 1})
sec = d["eval_duration"] / 1e9
print(d["message"]["content"][:80].replace("\n", " "), "...")
print(f"토큰 {d['eval_count']}개, 생성 {sec:.1f}초 = {d['eval_count'] / sec:.0f}토큰/초")

print("## 2. 옵션 넘기기: temperature 0.2 와 num_ctx 4096")
d = chat("로컬 AI의 장점을 한 문장으로 말해 주세요.", options={"temperature": 0.2, "num_ctx": 4096, "seed": 1})
print(d["message"]["content"].strip())

print("## 3. JSON 형식 고정: 문장 네 개에서 날짜와 장소 뽑기")
schema = {"type": "object",
          "properties": {"date": {"type": "string"}, "place": {"type": "string"}},
          "required": ["date", "place"]}
texts = ["다음 주 화요일 오후 3시에 서울 본사 3층 회의실에서 만납니다.",
         "10월 30일 아침 9시에 부산 지사 대강당에서 교육이 있습니다.",
         "내일 점심에 판교 사무실 1층 카페에서 보기로 했습니다.",
         "금요일 오후 2시 온라인으로 진행하며 장소는 따로 없습니다."]
ok = 0
for t in texts:
    d = chat(f"다음 문장에서 날짜와 장소를 뽑아 주세요: '{t}'", format=schema, options={"temperature": 0})
    try:
        j = json.loads(d["message"]["content"])
        ok += set(j) == {"date", "place"}
        print(" ", j)
    except json.JSONDecodeError:
        print("  파싱 실패:", d["message"]["content"][:60])
print(f"구조가 맞은 답: {ok}/{len(texts)}  (값이 맞는지는 따로 사람이 봐야 한다)")

print("## 4. 스트리밍")
t0 = time.time()
first = None
n = 0
text = ""
with requests.post(f"{URL}/api/chat", stream=True, json={
        "model": MODEL, "stream": True,
        "messages": [{"role": "user", "content": "로컬 AI의 장점 두 가지를 말해 주세요."}]}) as r:
    for line in r.iter_lines():
        c = json.loads(line)
        if c["message"]["content"] and first is None:
            first = time.time() - t0
        text += c["message"]["content"]
        n += 1
print(text[:60].replace("\n", " "), "...")
print(f"첫 조각 {first:.2f}초, 조각 {n}개, 전체 {time.time() - t0:.1f}초")
