"""파일 목록에서 패킹이 의심되는 것을 골라 종료 코드로 알려 줍니다.

판정 기준(둘 중 하나라도 해당하면 의심):
  1) PE 파일에서 섹션 이름이 UPX 로 시작하거나, 파일 내 크기 512바이트 이상 섹션의 엔트로피가 임계값 이상
  2) PE 가 아닌 파일은 파일 전체 엔트로피가 임계값 이상(압축, 암호화 자료도 걸립니다)
종료 코드: 0 의심 없음, 1 의심 파일 있음
실행: python scan_packed.py [--threshold 7.0] 파일 또는 폴더 ...
파일은 읽기만 하며 실행하지 않습니다.
"""
import argparse
import math
import sys
from collections import Counter
from pathlib import Path

import pefile


def shannon(data: bytes) -> float:
    if not data:
        return 0.0
    n = len(data)
    return max(0.0, -sum(c / n * math.log2(c / n) for c in Counter(data).values()))


def judge(path: Path, threshold: float):
    """(종류, 엔트로피, 사유 목록)을 돌려줍니다."""
    raw = path.read_bytes()
    try:
        pe = pefile.PE(data=raw, fast_load=True)
    except pefile.PEFormatError:
        h = shannon(raw)
        return "기타", h, ([f"파일 전체 엔트로피 {h:.2f}"] if h >= threshold else [])
    reasons = []
    top = 0.0
    for s in pe.sections:
        name = s.Name.rstrip(b"\x00").decode("ascii", "replace")
        h = shannon(s.get_data())
        top = max(top, h) if s.SizeOfRawData >= 512 else top
        if name.upper().startswith("UPX"):
            reasons.append(f"섹션 이름 {name}")
        if s.SizeOfRawData >= 512 and h >= threshold:
            reasons.append(f"섹션 {name} 엔트로피 {h:.2f}")
    return "PE", top, reasons


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--threshold", type=float, default=7.0)
    ap.add_argument("paths", nargs="+")
    a = ap.parse_args()
    files = []
    for p in map(Path, a.paths):
        files += sorted(x for x in p.rglob("*") if x.is_file()) if p.is_dir() else [p]
    flagged = 0
    print(f"{'파일':<22} {'종류':<4} {'최대 엔트로피':>12}  판정")
    for f in files:
        kind, h, reasons = judge(f, a.threshold)
        flagged += bool(reasons)
        print(f"{f.name:<22} {kind:<4} {h:>12.2f}  {'의심: ' + ', '.join(reasons) if reasons else '-'}")
    print(f"임계값 {a.threshold}, 의심 {flagged}건 / 전체 {len(files)}건")
    return 1 if flagged else 0


if __name__ == "__main__":
    sys.exit(main())
