"""네 가지 스캔 방식을 같은 정답표로 채점하고, 마스킹한 결과를 보여 줍니다.

사용법: python compare.py [--detail] [--mask 파일이름]
출력에는 원래 값을 찍지 않습니다. 스캔 결과 파일도 개인정보가 되기 때문입니다.
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

import scan_presidio
import scan_regex

DATA = Path("data")
KINDS = ["RRN", "PHONE", "EMAIL", "BRN", "CARD"]
KEEP = {"RRN": 6, "CARD": 6, "BRN": 3}   # 앞에서 남길 숫자 개수(전화번호는 뒤 8자리를 가림)


def mask_value(kind, text):
    if kind == "EMAIL":
        return "***@" + text.split("@", 1)[1] if "@" in text else "(문자로 풀어 쓴 표기)"
    left, out = KEEP.get(kind, 0), []
    if kind == "PHONE":
        left = len(scan_regex.digits(text)) - 8          # 뒤 8자리만 가립니다
    for ch in text:
        if ch.isdigit():
            out.append(ch if left > 0 else "*")
            left -= 1
        else:
            out.append(ch)
    return "".join(out)


RRN_SHAPE = re.compile(r"(?<!\d)(\d{6}[- ]?)[1-4]\d{6}(?!\d)")


def hide_rrn_shape(text):
    """탐지 여부와 상관없이 주민등록번호 모양(6자리 + 7자리)은 앞 6자리만 남기고 가립니다."""
    return RRN_SHAPE.sub(lambda m: m.group(1) + "*" * 7, text)


def pad(text, width):
    """한글은 두 칸으로 세어 표 칸을 맞춥니다."""
    return text + " " * (width - sum(2 if ord(c) > 0x2E7F else 1 for c in text))


def merge(found):
    """같은 종류끼리 겹치는 결과는 하나로 합칩니다."""
    out = []
    for f in sorted(found, key=lambda x: (x["type"], x["start"])):
        if out and out[-1]["type"] == f["type"] and f["start"] < out[-1]["end"]:
            out[-1]["end"] = max(out[-1]["end"], f["end"])
        else:
            out.append(dict(f))
    return out


def overlap(a, b):
    return a["type"] == b["type"] and a["start"] < b["end"] and b["start"] < a["end"]


def load_texts():
    return {p.name: p.read_text(encoding="utf-8") for p in sorted(DATA.iterdir()) if p.suffix in (".csv", ".txt")}


def run_all(texts):
    plain, strict = {}, {}
    pres_base, pres_kr, other = {}, {}, Counter()
    eng_base, eng_kr = scan_presidio.build(False), scan_presidio.build(True)
    for name, text in texts.items():
        plain[name] = scan_regex.scan_text(text, False)
        strict[name] = scan_regex.scan_text(text, True)
        pres_base[name], _ = scan_presidio.scan_text(eng_base, text)
        pres_kr[name], o = scan_presidio.scan_text(eng_kr, text)
        other.update(o)
    return [("형식만 정규식", plain), ("검증 정규식", strict),
            ("Presidio 기본", pres_base), ("Presidio+한국어", pres_kr)], other


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    detail = "--detail" in sys.argv
    texts = load_texts()
    truth = json.loads((DATA / "labels.json").read_text(encoding="utf-8"))
    scanners, other = run_all(texts)
    if "--mask" in sys.argv:
        name = sys.argv[sys.argv.index("--mask") + 1]
        text = texts[name]
        found = sorted(merge(dict(scanners)["검증 정규식"][name]), key=lambda x: -x["start"])
        for f in found:
            text = text[:f["start"]] + mask_value(f["type"], text[f["start"]:f["end"]]) + text[f["end"]:]
        text = hide_rrn_shape(text)                      # 정규식이 놓친 값도 출력 전에 한 번 더 가립니다
        out = Path("out")
        out.mkdir(exist_ok=True)
        (out / name).write_text(text, encoding="utf-8", newline="\n")
        print(f"--- out/{name} (검증 정규식 결과로 가림)")
        print(text, end="")
        return

    print(f"정답 {len(truth)}건 (RRN {sum(t['type']=='RRN' for t in truth)}, "
          f"PHONE {sum(t['type']=='PHONE' for t in truth)}, EMAIL {sum(t['type']=='EMAIL' for t in truth)}, "
          f"BRN {sum(t['type']=='BRN' for t in truth)}, CARD {sum(t['type']=='CARD' for t in truth)})\n")
    print(pad("방식", 18) + f"{'탐지':>5}{'정탐':>5}{'오탐':>5}{'미탐':>5}")
    results = {}
    for label, per_file in scanners:
        tp = fp = fn = det = 0
        miss, wrong, hit_kind = [], [], Counter()
        for name in texts:
            found = merge(per_file[name])
            det += len(found)
            tr = [t for t in truth if t["file"] == name]
            for t in tr:
                if any(overlap(t, f) for f in found):
                    tp += 1
                    hit_kind[t["type"]] += 1
                else:
                    miss.append((name, t))
            for f in found:
                if not any(overlap(t, f) for t in tr):
                    wrong.append((name, f))
        fp, fn = len(wrong), len(miss)
        results[label] = (hit_kind, miss, wrong)
        print(pad(label, 18) + f"{det:>5}{tp:>5}{fp:>5}{fn:>5}")
    print("\n종류별 정탐 수 (정답 수 대비)")
    totals = Counter(t["type"] for t in truth)
    print(pad("방식", 18) + "".join(f"{k:>8}" for k in KINDS))
    for label, _ in scanners:
        hk = results[label][0]
        print(pad(label, 18) + "".join(f"{hk[k]:>4}/{totals[k]:<3}" for k in KINDS))
    print("\nPresidio 가 개인정보 5종 밖에서 낸 엔티티(임계값 0.5 이상):", dict(other))
    scores = Counter(f["score"] for fs in scanners[3][1].values() for f in merge(fs) if f["type"] == "RRN")
    print("Presidio+한국어의 RRN 점수 분포:", dict(sorted(scores.items(), reverse=True)))
    if detail:
        for label, _ in scanners:
            if label == "Presidio 기본":
                continue                                  # 미탐이 너무 많아 목록은 생략합니다
            _, miss, wrong = results[label]
            print(f"\n[{label}] 오탐 {len(wrong)}건")
            for name, f in wrong:
                v = texts[name][f["start"]:f["end"]]
                print(f"  {name} {f['type']} {mask_value(f['type'], v)}")
            print(f"[{label}] 미탐 {len(miss)}건")
            for name, t in miss:
                v = t["text"]
                shown = mask_value(t["type"], v) if t["type"] == "EMAIL" or any(c.isdigit() for c in v) else "(한글로 쓴 숫자)"
                print(f"  {name} {t['type']} {shown}")


if __name__ == "__main__":
    main()
