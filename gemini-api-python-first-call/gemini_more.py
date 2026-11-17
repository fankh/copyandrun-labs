"""Gemini API 심화: 언어별 토큰 수, 출력 길이 제한과 종료 이유, 같은 질문의 반복 결과, 응답 시간, 생각 토큰.

준비: pip install google-genai, 환경 변수 GEMINI_API_KEY (코드에 적지 않는다)
주의: 호출을 약 30번 보낸다. 무료 한도가 작은 키에서는 중간에 429 오류가 날 수 있다.
실행: python -X utf8 gemini_more.py   (약 1분)
"""
import statistics
import time

from google import genai
from google.genai import types

MODEL = "gemini-2.5-flash-lite"
c = genai.Client()

print("## 1. 같은 뜻의 글, 언어별 토큰 수(count_tokens)")
samples = {
    "한국어 문장": "오늘은 날씨가 좋아서 공원에서 산책을 하며 사진을 찍었습니다.",
    "영어 문장": "The weather was nice today, so I took a walk in the park and took photos.",
    "한국어 용어": "취약점 점검과 침투 시험의 차이를 설명해 주세요.",
    "영어 용어": "Explain the difference between vulnerability scanning and penetration testing.",
    "파이썬 코드": "def add(a, b):\n    return a + b\n\nprint(add(1, 2))",
    "숫자 나열": "1234567890 " * 5,
}
print(f"  {'종류':<10}{'글자 수':>8}{'토큰 수':>8}{'글자/토큰':>10}")
for name, text in samples.items():
    n = c.models.count_tokens(model=MODEL, contents=text).total_tokens
    print(f"  {name:<10}{len(text):>8}{n:>8}{len(text) / n:>10.2f}")

print("\n## 2. 출력 길이를 제한하면(max_output_tokens=12) 어떻게 끝나는가")
for limit in (12, 1500):
    r = c.models.generate_content(model=MODEL, contents="한국어로 로컬 AI의 장점을 다섯 가지 설명해 주세요.",
                                  config=types.GenerateContentConfig(max_output_tokens=limit))
    fr = r.candidates[0].finish_reason
    print(f"  한도 {limit:>3}: 종료 이유 {getattr(fr, 'name', fr)}, 출력 토큰 {r.usage_metadata.candidates_token_count}, 끝 글자 {r.text.strip()[-12:]!r}")

print("\n## 3. 같은 질문 5번: temperature 0 과 1.5 에서 서로 다른 답이 몇 개인가")
for temp in (0.0, 1.5):
    outs = []
    for _ in range(5):
        r = c.models.generate_content(model=MODEL, contents="동물 하나를 골라 이름만 한 단어로 답하세요.",
                                      config=types.GenerateContentConfig(temperature=temp))
        outs.append(r.text.strip())
    print(f"  temperature {temp}: {len(set(outs))}가지  {outs}")

print("\n## 4. 응답 시간(같은 질문 5번)")
ts = []
for _ in range(5):
    t = time.time()
    c.models.generate_content(model=MODEL, contents="한 문장으로 인사해 주세요.")
    ts.append(time.time() - t)
print(f"  최소 {min(ts):.2f}초, 중앙값 {statistics.median(ts):.2f}초, 최대 {max(ts):.2f}초")

print("\n## 5. 생각 토큰(thinking): 기본, 끔(0), 큰 예산(1024) 비교")
q = "17 곱하기 23은 얼마인가요? 풀이 과정도 한 줄로 쓰세요."
for label, cfg in (("기본", None), ("budget 0", types.ThinkingConfig(thinking_budget=0)),
                   ("budget 1024", types.ThinkingConfig(thinking_budget=1024))):
    conf = types.GenerateContentConfig(thinking_config=cfg) if cfg else None
    r = c.models.generate_content(model=MODEL, contents=q, config=conf)
    u = r.usage_metadata
    print(f"  {label:<12} 생각 토큰 {u.thoughts_token_count}, 출력 토큰 {u.candidates_token_count}, 답: {r.text.strip()[:40]!r}")
