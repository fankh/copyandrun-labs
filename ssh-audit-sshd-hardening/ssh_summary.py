#!/usr/bin/env python3
"""ssh-audit -j 의 JSON 을 읽어 분류별 fail, warn 개수를 세고, 기준을 넘으면 종료 코드 1 로 끝낸다.
사용: python ssh_summary.py weak.json [--max-fail 0] [--max-warn 99] [--list]"""
import json
import sys

sys.stdout.reconfigure(encoding="utf-8")
args = sys.argv[1:]
opt = lambda name, default: int(args[args.index(name) + 1]) if name in args else default
max_fail, max_warn = opt("--max-fail", 0), opt("--max-warn", 99)
d = json.load(open(args[0], encoding="utf-8"))
tf = tw = 0
print(f"== {args[0]}   서버 배너: {d['banner'].get('raw', '')}")
for cat, label in (("kex", "키 교환"), ("key", "호스트 키"), ("enc", "암호"), ("mac", "MAC")):
    f = [a["algorithm"] for a in d[cat] if a.get("notes", {}).get("fail")]
    w = [a["algorithm"] for a in d[cat] if a.get("notes", {}).get("warn") and not a.get("notes", {}).get("fail")]
    tf += len(f)
    tw += len(w)
    print(f"  {label:<6} 전체 {len(d[cat]):>2}개  fail {len(f):>2}  warn {len(w):>2}")
    if "--list" in args:
        for name in f:
            print(f"      fail  {name}")
print(f"  합계 fail {tf}개, warn {tw}개 (허용 fail {max_fail}, warn {max_warn})")
ok = tf <= max_fail and tw <= max_warn
print("  판정:", "통과" if ok else "미달")
sys.exit(0 if ok else 1)
