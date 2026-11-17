#!/usr/bin/env python3
"""semgrep 의 JSON 결과를 규칙별로 세고, ERROR 가 하나라도 있으면 종료 코드 1로 끝낸다.
사용: python semgrep_summary.py out.json   (WARNING 은 세기만 하고 게이트에는 쓰지 않는다)"""
import collections
import json
import sys

sys.stdout.reconfigure(encoding="utf-8")

data = json.load(open(sys.argv[1], encoding="utf-8"))
count = collections.Counter()
levels = collections.Counter()
for r in data["results"]:
    rule = r["check_id"].split(".")[-1]
    level = r["extra"]["severity"]
    count[(level, rule)] += 1
    levels[level] += 1
for (level, rule), n in sorted(count.items()):
    print(f"  {level:<8} {n}건  {rule}")
print(f"  합계 {sum(levels.values())}건 (ERROR {levels['ERROR']}, WARNING {levels['WARNING']})")
sys.exit(1 if levels["ERROR"] else 0)
