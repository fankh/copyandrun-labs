"""Gemini API 첫 호출: 응답, 토큰 사용량, 토큰 세기, 오류 두 가지를 한 번에 확인한다.

준비:
  pip install google-genai requests
  환경 변수 GEMINI_API_KEY 에 키를 넣어 둔다(코드에 적지 않는다).
실행:
  python -X utf8 first_call.py
"""
import os
import requests
from google import genai
from google.genai import errors

MODEL = "gemini-2.5-flash-lite"
c = genai.Client()  # GEMINI_API_KEY 환경 변수를 자동으로 읽는다

print("== 1. 첫 응답")
r = c.models.generate_content(model=MODEL, contents="한국어로 한 문장만 자기소개 해 주세요.")
print(r.text.strip())
u = r.usage_metadata
print("입력 %s, 출력 %s, 합계 %s" % (u.prompt_token_count, u.candidates_token_count, u.total_token_count))

print("== 2. 보내기 전에 토큰 세기")
ct = c.models.count_tokens(model=MODEL, contents="한국어로 토큰을 세어 봅니다.")
print("total_tokens", ct.total_tokens)

print("== 3. 모델 이름을 틀렸을 때")
try:
    c.models.generate_content(model="gemini-no-such-model", contents="hi")
except errors.ClientError as e:
    print(type(e).__name__, e.code, e.status)

print("== 4. 키가 틀렸을 때(REST로 직접 호출)")
resp = requests.post(
    "https://generativelanguage.googleapis.com/v1beta/models/%s:generateContent" % MODEL,
    headers={"x-goog-api-key": "not-a-real-key", "content-type": "application/json"},
    json={"contents": [{"parts": [{"text": "hi"}]}]}, timeout=30)
err = resp.json().get("error", {})
print(resp.status_code, err.get("status"), "|", err.get("message", "")[:60])

print("== 5. 이 키로 조회되는 모델 수")
print(sum(1 for _ in c.models.list()), "개 (이름은 시간이 지나면 바뀐다)")
print("키 환경 변수 설정 여부:", bool(os.environ.get("GEMINI_API_KEY")))
