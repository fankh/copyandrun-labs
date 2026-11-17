"""Gemini API 스트리밍, 대화 세션, 대화가 길어질 때 입력 토큰이 느는 모습을 확인한다.

준비:
  pip install google-genai
  환경 변수 GEMINI_API_KEY 에 키를 넣어 둔다.
실행:
  python -X utf8 stream_chat.py
"""
import time
from google import genai

MODEL = "gemini-2.5-flash-lite"
c = genai.Client()

print("== 1. 스트리밍: 첫 조각이 오기까지의 시간")
t = time.time()
first = None
n = 0
txt = ""
for ch in c.models.generate_content_stream(
        model=MODEL, contents="로컬 AI와 클라우드 AI의 차이를 두 문장으로 설명해 주세요."):
    if ch.text and first is None:
        first = time.time() - t
    n += 1
    txt += ch.text or ""
print("첫 조각 %.2fs, 조각 %d개, 전체 %.2fs" % (first, n, time.time() - t))
print(txt.strip())

print("== 2. 매 호출은 독립: 세션 없이 두 번 부르기")
c.models.generate_content(model=MODEL, contents="제 이름은 민수입니다. 기억해 주세요.")
print(c.models.generate_content(model=MODEL, contents="제 이름이 뭐라고 했죠?").text.strip()[:80])

print("== 3. 대화 세션: 이전 대화를 기억")
chat = c.chats.create(model=MODEL)
chat.send_message("제 이름은 민수입니다. 기억해 주세요.")
print(chat.send_message("제 이름이 뭐라고 했죠?").text.strip())

print("== 4. 세션의 비용: 턴이 쌓일수록 입력 토큰이 늘어난다")
chat = c.chats.create(model=MODEL)
for i in range(1, 6):
    r = chat.send_message("보안 점검 항목 %d번째를 한 문장으로 알려 주세요." % i)
    print("턴 %d 입력 토큰 %s, 출력 토큰 %s"
          % (i, r.usage_metadata.prompt_token_count, r.usage_metadata.candidates_token_count))
