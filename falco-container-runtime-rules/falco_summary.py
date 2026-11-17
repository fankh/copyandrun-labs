#!/usr/bin/env python3
"""Falco 의 JSON 출력(한 줄에 이벤트 하나)을 읽어 컨테이너별, 규칙별로 세고, 지정한 컨테이너에서 LAB 규칙이 걸리면 종료 코드 1 로 끝낸다.
사용: python falco_summary.py falco.log 점검할컨테이너 [--expect N]"""
import collections
import json
import sys

sys.stdout.reconfigure(encoding="utf-8")
path, target = sys.argv[1], sys.argv[2]
expect = int(sys.argv[sys.argv.index("--expect") + 1]) if "--expect" in sys.argv else 0
count = collections.Counter()
for line in open(path, encoding="utf-8", errors="replace"):
    line = line.strip()
    if not line.startswith("{"):
        continue
    try:
        e = json.loads(line)
    except ValueError:
        continue
    f = e.get("output_fields", {})
    if f.get("container.name") == target and e.get("rule", "").startswith("LAB"):
        count[e["rule"]] += 1
total = sum(count.values())
print(f"  [{target}]")
for rule, n in sorted(count.items()):
    print(f"    {n}건  {rule}")
print(f"    합계 {total}건 (허용 {expect}건)")
sys.exit(1 if total > expect else 0)
