"""osv-scanner 의 JSON 결과를 패키지별로 요약하고, 지적을 모두 없애는 최소 버전을 계산한다.
사용: python osv_summary.py out.json
"""
import json
import sys
from collections import defaultdict


def ver(s):
    """'1.24.3' -> (1, 24, 3). 숫자가 아닌 꼬리표는 무시한다."""
    out = []
    for part in s.split("."):
        digits = "".join(ch for ch in part if ch.isdigit())
        out.append(int(digits) if digits else 0)
    return tuple(out)


def fixed_versions(vuln, name):
    """한 지적(vuln)에서 패키지 name 에 해당하는 수정 버전 목록."""
    found = []
    for aff in vuln.get("affected", []):
        if aff.get("package", {}).get("name", "").lower() != name.lower():
            continue
        for rng in aff.get("ranges", []):
            if rng.get("type") == "GIT":  # 커밋 해시는 버전이 아니므로 뺀다
                continue
            for ev in rng.get("events", []):
                if "fixed" in ev:
                    found.append(ev["fixed"])
    return found


data = json.load(open(sys.argv[1], encoding="utf-8"))
rows = defaultdict(lambda: {"ids": set(), "max": 0.0, "fixes": []})

for res in data["results"]:
    for pkg in res["packages"]:
        name, version = pkg["package"]["name"], pkg["package"]["version"]
        key = (pkg["package"]["ecosystem"], name, version)
        for grp in pkg["groups"]:
            rows[key]["ids"].add(grp["ids"][0])
            try:
                rows[key]["max"] = max(rows[key]["max"], float(grp["max_severity"]))
            except ValueError:
                pass
        for v in pkg["vulnerabilities"]:
            rows[key]["fixes"] += fixed_versions(v, name)

print(f"{'ecosystem':9} {'package':9} {'version':8} {'count':>5} {'max CVSS':>8}  one version that clears all")
for (eco, name, version), r in sorted(rows.items()):
    best = max(r["fixes"], key=ver) if r["fixes"] else "-"
    print(f"{eco:9} {name:9} {version:8} {len(r['ids']):>5} {r['max']:>8}  {best}")
print("total advisories:", sum(len(r["ids"]) for r in rows.values()))
