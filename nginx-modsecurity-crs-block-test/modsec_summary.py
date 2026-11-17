#!/usr/bin/env python3
"""요청 결과(TSV)와 ModSecurity 감사 로그(JSON 줄)를 읽어 모드별로 요약하고, 게이트 판정을 종료 코드로 돌려준다.
사용: python modsec_summary.py results.tsv audit-On-1.json   (게이트: 공격 전부 차단 + 정상 요청 차단 0건)"""
import collections
import json
import sys

sys.stdout.reconfigure(encoding="utf-8")

rows = [line.rstrip("\n").split("\t") for line in open(sys.argv[1], encoding="utf-8") if line.strip()]
attacks = [r for r in rows if r[0] == "A"]
benign = [r for r in rows if r[0] == "B"]
blocked_a = [r[1] for r in attacks if r[2] == "403"]
blocked_b = [r[1] for r in benign if r[2] == "403"]
print(f"  공격 {len(blocked_a)}/{len(attacks)}건 차단, 정상 요청 {len(blocked_b)}/{len(benign)}건 오차단")
if blocked_b:
    print("  오차단된 정상 요청: " + ", ".join(blocked_b))

if len(sys.argv) > 2:
    ids = collections.Counter()
    for line in open(sys.argv[2], encoding="utf-8"):
        if line.startswith('{"transaction"'):
            for m in json.loads(line)["transaction"].get("messages", []):
                ids[(m["details"]["ruleId"], m["message"][:48])] += 1
    for (rid, msg), n in ids.most_common(6):
        print(f"  규칙 {rid} {n:>2}회  {msg}")

ok = len(blocked_a) == len(attacks) and not blocked_b
print("  게이트:", "통과" if ok else "실패")
sys.exit(0 if ok else 1)
