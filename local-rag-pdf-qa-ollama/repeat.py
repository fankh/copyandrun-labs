# repeat.py
import sys
from collections import Counter

import rag

index = rag.build_index(sys.argv[1])
RUNS = 10
questions = [
    "재택근무는 일주일에 몇 번까지 가능한가요?",
    "회사 주차장 이용 요금은 얼마인가요?",
    "육아휴직은 최대 몇 개월인가요?",
    "점심 시간은 몇 시부터인가요?",
]
for q in questions:
    counts = Counter(rag.ask(index, q)[0] for _ in range(RUNS))
    print(f"{RUNS}회 중 서로 다른 답 {len(counts)}종 | {q}")
    for ans, n in counts.most_common():
        print(f"    {n}회: {ans[:70]}")
a = rag.embed(["search_query: 테스트"])[0]
b = rag.embed(["search_query: 테스트"])[0]
print("같은 문장의 임베딩 두 번이 완전히 같은가:", a == b)
