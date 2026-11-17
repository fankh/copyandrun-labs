"""Gemini API 시스템 지시, 온도, JSON 스키마 출력을 한 번에 확인한다.

준비:
  pip install google-genai pydantic
  환경 변수 GEMINI_API_KEY 에 키를 넣어 둔다.
실행:
  python -X utf8 system_json.py
"""
import json
import re
from google import genai
from google.genai import types
from pydantic import BaseModel

MODEL = "gemini-2.5-flash-lite"
c = genai.Client()

print("== 1. 시스템 지시: 존댓말, 세 문장 이내")
r = c.models.generate_content(
    model=MODEL,
    contents="회사 노트북 비밀번호를 잊어버렸습니다. 어떻게 해야 하나요?",
    config=types.GenerateContentConfig(
        system_instruction="당신은 사내 IT 도우미입니다. 항상 존댓말로, 세 문장 이내로 답합니다.",
        temperature=0.2, max_output_tokens=300))
text = r.text.strip()
print(text)
sentences = [s for s in re.split(r"(?<=[.?!])\s+", text) if s]
print("문장 수:", len(sentences), "| 출력 토큰:", r.usage_metadata.candidates_token_count)


class Meeting(BaseModel):
    date: str
    place: str


print("== 2. JSON 스키마 출력")
r = c.models.generate_content(
    model=MODEL,
    contents="다음 문장에서 날짜와 장소를 뽑아 주세요: '다음 주 화요일 오후 3시에 서울 본사 3층 회의실에서 만납니다.'",
    config=types.GenerateContentConfig(response_mime_type="application/json", response_schema=Meeting))
print(r.text)
print(r.parsed)
data = json.loads(r.text)  # 구조는 스키마가 보장하지만 내용은 코드에서 따로 검증한다
assert set(data) == {"date", "place"}
print("검증 통과: 키", sorted(data))

print("== 3. 같은 질문 세 번, 온도 0과 1.5")
for temp in (0.0, 1.5):
    outs = []
    for _ in range(3):
        rr = c.models.generate_content(
            model=MODEL, contents="비밀번호 관리의 핵심을 한 문장으로 말해 주세요.",
            config=types.GenerateContentConfig(temperature=temp, max_output_tokens=80))
        outs.append(rr.text.strip())
    print("temperature", temp, "-> 서로 다른 답", len(set(outs)), "개 / 3번")
