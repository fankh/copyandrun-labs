"""capa 의 JSON 결과(json/*.json)를 읽어 프로그램별 기능 규칙을 표로 요약한다.

사용법: python3 summarize.py json/empty.json json/fileio.json json/sockdemo.json
표준 라이브러리만 쓴다.
"""
import json
import sys
from pathlib import Path


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def rule_rows(doc):
    """규칙마다 (이름, 이름공간, 일치 횟수, ATT&CK ID 목록, MBC ID 목록)을 만든다."""
    rows = []
    for rule in doc["rules"].values():
        meta = rule["meta"]
        if meta.get("lib"):
            continue  # 다른 규칙의 부품으로만 쓰이는 라이브러리 규칙은 뺀다
        attack = [a["id"] for a in meta.get("attack", [])]
        mbc = [m["id"] for m in meta.get("mbc", [])]
        rows.append((meta["name"], meta.get("namespace", ""),
                     len(rule["matches"]), attack, mbc))
    return sorted(rows, key=lambda r: (r[1], r[0]))


def main(paths):
    for path in paths:
        doc = load(path)
        name = Path(path).stem
        rows = rule_rows(doc)
        print(f"== {name}: 기능 규칙 {len(rows)}개")
        print(f"{'규칙':<46} {'일치':>4}  {'ATT&CK':<8} MBC")
        for rule_name, _ns, n, attack, mbc in rows:
            print(f"{rule_name[:46]:<46} {n:>4}  {','.join(attack) or '-':<8} {','.join(mbc) or '-'}")
        print()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("사용법: python3 summarize.py json/<파일>.json ...")
    main(sys.argv[1:])
