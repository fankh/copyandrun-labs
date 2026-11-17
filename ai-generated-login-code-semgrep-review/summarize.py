"""Semgrep JSON 결과를 파일, 줄, 규칙 이름으로 요약합니다. 직접 쓴 규칙은 custom, 레지스트리 규칙은 registry 로 표시합니다."""
import json
import sys
from collections import Counter

data = json.load(open(sys.argv[1], encoding="utf-8"))
rows = []
for r in data["results"]:
    rule = r["check_id"].split(".")[-1]
    rows.append((r["path"], r["start"]["line"], "custom" if rule.startswith("login-") else "registry", rule))
rows.sort()
for path, line, src, rule in rows:
    print(f"{path:<12}{line:>4}  {src:<10}{rule}")
if not rows:
    print("탐지 0건")
print()
for path, n in sorted(Counter(r[0] for r in rows).items()):
    print(f"{path}: {n}건")
print(f"합계: {len(rows)}건")
