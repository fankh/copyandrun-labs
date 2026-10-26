# evaluate.py
import re
import sys

import rag

# (질문, 정답 조항에 들어 있는 핵심 문구, 답변 판정 정규식)
# 판정은 숫자와 단위가 정확히 일치해야 합니다. (?<!\d) 는 앞에 다른 숫자가 붙은 경우(15일, 11만 5천 원)를 걸러 냅니다.
CASES = [
    ("재택근무는 일주일에 몇 번까지 가능한가요?", "주 2회", r"주 2회"),
    ("지각은 몇 시 이후 출근을 말하나요?", "9시 10분", r"(?<!\d)9시 10분"),
    ("본인 결혼 휴가는 며칠인가요?", "본인 결혼은 5일", r"(?<!\d)5일"),
    ("병가는 연 며칠까지 쓸 수 있나요?", "연 10일", r"(?<!\d)10일"),
    ("비밀번호는 몇 일마다 바꾸나요?", "90일마다", r"(?<!\d)90일"),
    ("개인 클라우드에 업무 파일을 올려도 되나요?", "금지한다", r"금지|안 됩니다"),
    ("야근 식대는 얼마까지 인정되나요?", "1만 5천 원", r"(?<!\d)1만 5천 원"),
    ("비용 청구는 언제까지 하나요?", "다음 달 5일", r"다음 달 5일"),
]
pdf = sys.argv[1]
index = rag.build_index(pdf)
print(f"방식={rag.os.environ.get('CHUNKING', 'article')} 조각={len(index)}개")
found = ok = 0
for q, key, pattern in CASES:
    hits = rag.search(index, q)
    got = any(key in h["text"].replace("\n", "") for h in hits)
    found += got
    ans, _ = rag.ask(index, q)
    good = re.search(pattern, ans) is not None
    ok += good
    print(f"검색={'성공' if got else '실패'} 답={'성공' if good else '실패'} | {q} -> {ans}")
print(f"검색 적중 {found}/{len(CASES)}, 답이 정답과 일치 {ok}/{len(CASES)}")
