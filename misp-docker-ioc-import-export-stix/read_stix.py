"""STIX 2.1 번들을 읽어 객체 종류별 개수와 indicator 의 패턴을 보여 줍니다. 표준 라이브러리만 씁니다.

사용법: python read_stix.py out.json
"""
import json
import sys
from collections import Counter

bundle = json.load(open(sys.argv[1], encoding="utf-8"))
objs = bundle["objects"]
print("번들", bundle["id"], "| 형식", bundle["type"], "| 객체", len(objs), "개")

print("\n[1] 객체 종류별 개수")
for kind, n in sorted(Counter(o["type"] for o in objs).items()):
    print(f"  {kind:<20}{n}")

print("\n[2] indicator 패턴")
for o in objs:
    if o["type"] == "indicator":
        print(f"  {o['pattern']}")
        print(f"      spec {o['spec_version']} | 유효 시작 {o['valid_from'][:19]} | 레이블 {[l for l in o.get('labels', []) if l.startswith('lab:')]}")

print("\n[3] observed-data 가 가리키는 값과 indicator 유무")
by_id = {o["id"]: o for o in objs}
patterns = " ".join(o["pattern"] for o in objs if o["type"] == "indicator")
for o in objs:
    if o["type"] != "observed-data":
        continue
    for ref in o.get("object_refs", []):
        t = by_id.get(ref, {})
        if t.get("type") in ("domain-name", "url", "ipv4-addr", "file", "email-message"):
            value = t.get("value") or t.get("name") or t.get("subject")
            if not value and t.get("hashes"):
                value = next(iter(t["hashes"].values()))
            mark = "indicator 있음" if value in patterns else "indicator 없음"
            print(f"  {t['type']:<14}{str(value)[:44]:<46}{mark}")
