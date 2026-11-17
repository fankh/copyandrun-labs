"""testssl.sh 의 JSON 결과를 읽어 심각도별 개수를 세고, 기준 이상의 지적이 있으면 종료 코드 1을 돌려준다.
사용: python testssl_summary.py bad.json good.json [--fail-on HIGH] [--ignore id1,id2] [--show LOW]
"""
import argparse
import json
import os
import sys
from collections import Counter

ORDER = ["OK", "INFO", "LOW", "MEDIUM", "HIGH", "CRITICAL"]  # 오른쪽일수록 심각

ap = argparse.ArgumentParser()
ap.add_argument("files", nargs="+")
ap.add_argument("--fail-on", default="HIGH", help="이 등급 이상이 남아 있으면 실패(기본 HIGH)")
ap.add_argument("--ignore", default="", help="쉼표로 구분한 항목 id. 예외로 두고 세지 않는다")
ap.add_argument("--show", default="LOW", help="이 등급 이상의 지적을 줄마다 보여 준다")
a = ap.parse_args()

ignore = {x for x in a.ignore.split(",") if x}
fail_at, show_at = ORDER.index(a.fail_on), ORDER.index(a.show)
failed = False

for path in a.files:
    items = json.load(open(path, encoding="utf-8"))
    kept = [x for x in items if x["id"] not in ignore and x["severity"] in ORDER]
    cnt = Counter(x["severity"] for x in kept)
    name = os.path.basename(path)
    line = "  ".join(f"{s}={cnt.get(s, 0)}" for s in reversed(ORDER))
    print(f"[{name}] {line}   (ignored ids: {len(ignore)})")
    for x in sorted(kept, key=lambda x: -ORDER.index(x["severity"])):
        if ORDER.index(x["severity"]) >= show_at:
            print(f"   {x['severity']:8} {x['id']:26} {x['finding'][:60]}")
    if any(ORDER.index(x["severity"]) >= fail_at for x in kept):
        failed = True

print("RESULT:", "FAIL" if failed else "PASS", f"(fail-on {a.fail_on})")
sys.exit(1 if failed else 0)
