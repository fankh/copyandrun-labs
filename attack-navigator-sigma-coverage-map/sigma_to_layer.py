import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

import yaml

# ATT&CK Enterprise 20.0 의 전술(행렬에 나오는 순서)
TACTICS = [
    "reconnaissance", "resource_development", "initial_access", "execution",
    "persistence", "privilege_escalation", "stealth", "defense_impairment",
    "credential_access", "discovery", "lateral_movement", "collection",
    "command_and_control", "exfiltration", "impact",
]
TECH = re.compile(r"^attack\.(t\d{4})(?:\.(\d{3}))?$", re.I)
SKIP_STATUS = {"deprecated", "unsupported"}


def load_rules(paths):
    files = []
    for p in paths:
        p = Path(p)
        files += sorted(p.rglob("*.yml")) if p.is_dir() else [p]
    for f in files:
        try:
            for doc in yaml.safe_load_all(f.read_text(encoding="utf-8")):
                if isinstance(doc, dict) and "title" in doc:
                    yield f, doc
        except yaml.YAMLError as e:
            print(f"읽지 못함: {f.name}: {str(e).splitlines()[0]}", file=sys.stderr)


def normalize(tag):
    """attack.t1059.001 -> T1059.001, 기법 태그가 아니면 None"""
    m = TECH.match(str(tag).strip())
    if not m:
        return None
    return m.group(1).upper() + ("." + m.group(2) if m.group(2) else "")


def load_attack(path):
    """ATT&CK STIX 파일에서 현재 기법 ID 와, 폐기된 ID 의 대체 ID 를 읽는다."""
    objs = json.loads(Path(path).read_text(encoding="utf-8"))["objects"]
    by_id = {o["id"]: o for o in objs}

    def ext_id(o):
        for r in o.get("external_references", []):
            if r.get("source_name") == "mitre-attack":
                return r.get("external_id")

    valid, old = set(), {}
    for o in objs:
        if o["type"] == "attack-pattern" and not o.get("revoked") and not o.get("x_mitre_deprecated"):
            valid.add(ext_id(o))
    for o in objs:
        if o["type"] == "relationship" and o["relationship_type"] == "revoked-by":
            src, dst = by_id.get(o["source_ref"]), by_id.get(o["target_ref"])
            if src and dst and src["type"] == "attack-pattern":
                old[ext_id(src)] = ext_id(dst)
    return valid, old


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--out", default="layer.json")
    ap.add_argument("--name", default="Sigma coverage")
    ap.add_argument("--expand", action="store_true", help="하위 기법을 펼친 채로 열기")
    ap.add_argument("--attack", help="ATT&CK STIX JSON 파일(있으면 없는 ID 를 알려 줌)")
    a = ap.parse_args()

    tech_rules = defaultdict(list)
    tactic_count = defaultdict(int)
    unknown_tactics = defaultdict(int)
    total = tagged = skipped = 0
    for f, rule in load_rules(a.paths):
        total += 1
        if str(rule.get("status", "")).lower() in SKIP_STATUS:
            skipped += 1
            continue
        tags = [str(t).lower().replace("-", "_") for t in (rule.get("tags") or [])]
        ids = {normalize(t) for t in tags} - {None}
        if ids:
            tagged += 1
        for t in ids:
            tech_rules[t].append(rule["title"])
        names = {t[len("attack."):] for t in tags if t.startswith("attack.")}
        for n in names:
            if n in TACTICS:
                tactic_count[n] += 1
            elif not re.match(r"^[a-z]{1,2}\d{4}", n):
                unknown_tactics[n] += 1

    techniques = []
    parents = {t.split(".")[0] for t in tech_rules if "." in t}
    for t in sorted(tech_rules):
        titles = tech_rules[t]
        comment = "규칙 %d개: %s" % (len(titles), "; ".join(titles[:3]) + (" ..." if len(titles) > 3 else ""))
        techniques.append({"techniqueID": t, "score": len(titles), "comment": comment, "enabled": True})
    if a.expand:
        for p in sorted(parents - set(tech_rules)):
            techniques.append({"techniqueID": p, "showSubtechniques": True})
        for item in techniques:
            if item["techniqueID"] in parents:
                item["showSubtechniques"] = True

    empty = [t for t in TACTICS if tactic_count[t] == 0]
    sums = defaultdict(int)  # 상위 기법 칸에는 하위 기법 규칙 수의 합이 표시된다
    for t, v in tech_rules.items():
        sums[t.split(".")[0]] += len(v)
    top = max(list(sums.values()) + [len(v) for v in tech_rules.values()] or [1])
    layer = {
        "name": a.name,
        "versions": {"attack": "20", "navigator": "5.3.2", "layer": "4.5"},
        "domain": "enterprise-attack",
        "description": "기법별 Sigma 규칙 개수. 규칙이 없는 전술: " + (", ".join(empty) or "없음"),
        "sorting": 0,
        "layout": {"layout": "side", "showName": True, "showID": True},
        "hideDisabled": False,
        "showAggregateScores": True,
        "aggregateFunction": "sum",
        "techniques": techniques,
        "gradient": {"colors": ["#ffffff", "#8ec6ff", "#1f5fbf"], "minValue": 0, "maxValue": top},
        "legendItems": [{"label": "규칙 개수가 많을수록 진한 파랑", "color": "#1f5fbf"}],
        "showTacticRowBackground": False,
        "selectTechniquesAcrossTactics": True,
    }
    Path(a.out).write_text(json.dumps(layer, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"규칙 {total}개 읽음, 기법 태그가 있는 규칙 {tagged}개, 건너뜀(deprecated/unsupported) {skipped}개")
    print(f"기법 {len(tech_rules)}개, 색 눈금 최댓값 {top}")
    print("기법별 규칙 수 상위:")
    for t, v in sorted(tech_rules.items(), key=lambda kv: (-len(kv[1]), kv[0]))[:8]:
        print(f"  {t:<10} {len(v)}")
    print("전술별 규칙 수:")
    for tac in TACTICS:
        n = tactic_count[tac]
        print(f"  {tac:<22} {n}" + ("   <- 규칙 없음" if n == 0 else ""))
    for n, c in sorted(unknown_tactics.items()):
        print(f"  알 수 없는 전술 태그 attack.{n}: 규칙 {c}개 (이름이 바뀌었을 수 있음)")
    if a.attack:
        valid, old = load_attack(a.attack)
        for t in sorted(set(tech_rules) - valid):
            hint = f" -> {old[t]} 로 바뀜" if t in old else " (현재 목록에 없음)"
            print(f"  경고 {t}: 규칙 {len(tech_rules[t])}개{hint}")
    print(f"레이어 저장: {a.out}")


if __name__ == "__main__":
    main()
