"""PE 파일의 섹션별 엔트로피, 섹션 이름, 임포트 수, 크기를 표로 보여 줍니다.

준비: pip install pefile
실행: python entropy_report.py hello_plain.exe hello_upx.exe
파일은 열어서 읽기만 하며 실행하지 않습니다.
"""
import math
import sys
from collections import Counter

import pefile


def shannon(data: bytes) -> float:
    """바이트 빈도로 Shannon 엔트로피를 구합니다(0.0 ~ 8.0, 단위는 비트/바이트)."""
    if not data:
        return 0.0
    n = len(data)
    return max(0.0, -sum(c / n * math.log2(c / n) for c in Counter(data).values()))


def report(path: str) -> None:
    raw = open(path, "rb").read()
    pe = pefile.PE(data=raw)
    imports = sum(len(e.imports) for e in getattr(pe, "DIRECTORY_ENTRY_IMPORT", []))
    dlls = len(getattr(pe, "DIRECTORY_ENTRY_IMPORT", []))
    print(f"== {path}")
    print(f"파일 크기 {len(raw)} 바이트, 파일 전체 엔트로피 {shannon(raw):.2f}")
    print(f"임포트 DLL {dlls}개, 임포트 함수 {imports}개")
    print(f"{'섹션':<8} {'파일 내 크기':>12} {'메모리 크기':>12} {'엔트로피':>8}")
    for s in pe.sections:
        name = s.Name.rstrip(b"\x00").decode("ascii", "replace")
        print(f"{name:<8} {s.SizeOfRawData:>12} {s.Misc_VirtualSize:>12} {shannon(s.get_data()):>8.2f}")


if __name__ == "__main__":
    for p in sys.argv[1:]:
        report(p)
