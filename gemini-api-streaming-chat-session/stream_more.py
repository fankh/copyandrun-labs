"""Gemini 스트리밍과 대화 기록 심화: 첫 조각까지의 시간, 조각 통계, 중간에 멈추기, 기록을 잘랐을 때 잊는 것.

준비: pip install google-genai, 환경 변수 GEMINI_API_KEY (코드에 적지 않는다)
실행: python -X utf8 stream_more.py   (약 1분)
"""
import statistics
import time

from google import genai
from google.genai import types

MODEL = "gemini-2.5-flash-lite"
c = genai.Client()
LONG = "로컬 AI와 클라우드 AI를 보안, 비용, 속도, 관리 네 가지 면에서 비교해 자세히 설명해 주세요."
CFG = types.GenerateContentConfig(thinking_config=types.ThinkingConfig(thinking_budget=0))

print("## 1. 스트리밍과 한 번에 받기: 첫 글자까지와 전체 시간(같은 긴 질문 4번씩)")
first, total_s, total_n = [], [], []
chunks_info = None
for _ in range(4):
    t = time.time()
    f = None
    n = 0
    sizes = []
    for ch in c.models.generate_content_stream(model=MODEL, contents=LONG, config=CFG):
        if f is None and ch.text:
            f = time.time() - t
        n += 1
        sizes.append(len(ch.text or ""))
    first.append(f)
    total_s.append(time.time() - t)
    chunks_info = (n, sizes)
for _ in range(4):
    t = time.time()
    c.models.generate_content(model=MODEL, contents=LONG, config=CFG)
    total_n.append(time.time() - t)
print(f"  스트리밍   첫 글자까지 중앙값 {statistics.median(first):.2f}초, 전체 중앙값 {statistics.median(total_s):.2f}초")
print(f"  한 번에    답을 받을 때까지 중앙값 {statistics.median(total_n):.2f}초 (그동안 화면에는 아무것도 없음)")

print("\n## 2. 조각 통계(마지막 스트리밍 한 번)")
n, sizes = chunks_info
print(f"  조각 {n}개, 평균 {statistics.mean(sizes):.0f}글자, 가장 긴 조각 {max(sizes)}글자, 첫 조각 {sizes[0]}글자")

print("\n## 3. 중간에 멈추기: 세 조각만 받고 끊기")
t = time.time()
got = ""
for i, ch in enumerate(c.models.generate_content_stream(model=MODEL, contents=LONG, config=CFG)):
    got += ch.text or ""
    if i == 2:
        break
print(f"  {time.time() - t:.2f}초 만에 {len(got)}글자만 받고 중단 (전체는 약 {statistics.median(total_s):.1f}초 걸림)")

print("\n## 4. 대화 기록(chat)과 기록을 자르면")
chat = c.chats.create(model=MODEL, config=CFG)
turns = ["제 이름은 지훈이고 가장 좋아하는 숫자는 47입니다. 기억해 주세요.",
         "대한민국의 수도는 어디인가요? 한 단어로.", "파이썬에서 리스트를 뒤집는 방법을 한 줄로 알려 주세요.",
         "HTTP 상태 코드 404는 무슨 뜻인가요? 한 문장으로.", "마지막으로, 제 이름과 가장 좋아하는 숫자가 뭐였죠?"]
ptoks = []
for q in turns:
    r = chat.send_message(q)
    ptoks.append(r.usage_metadata.prompt_token_count)
print(f"  기록을 전부 유지: 턴별 입력 토큰 {ptoks}")
print(f"  마지막 답: {r.text.strip()[:60]!r}")
hist = chat.get_history()
short = c.chats.create(model=MODEL, config=CFG, history=hist[-4:-1] if len(hist) >= 4 else hist)   # 최근 두 번의 주고받기만
r2 = short.send_message(turns[-1])
print(f"  기록을 최근 것만 남김: 입력 토큰 {r2.usage_metadata.prompt_token_count}, 답: {r2.text.strip()[:60]!r}")
