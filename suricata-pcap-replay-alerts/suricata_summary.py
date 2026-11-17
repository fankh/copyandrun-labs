#!/usr/bin/env python
"""eve.json 에서 alert 를 규칙(sid)별로 세고, 허용 개수를 넘으면 종료 코드 1 로 끝낸다.
사용: python suricata_summary.py eve.json [--max 0]"""
import collections
import json
import sys

sys.stdout.reconfigure(encoding="utf-8")

path = sys.argv[1]
limit = int(sys.argv[sys.argv.index("--max") + 1]) if "--max" in sys.argv else 0
count = collections.Counter()
for line in open(path, encoding="utf-8"):
    line = line.strip()
    if not line:
        continue
    ev = json.loads(line)
    if ev.get("event_type") == "alert":
        a = ev["alert"]
        count[(a["signature_id"], a["signature"])] += 1
total = sum(count.values())
for (sid, sig), n in sorted(count.items()):
    print(f"  sid {sid}  {n:>3}건  {sig}")
print(f"  합계 {total}건 (허용 {limit}건)")
sys.exit(1 if total > limit else 0)
