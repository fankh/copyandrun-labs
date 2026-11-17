"""정규식으로 한국어 개인정보를 찾습니다. validate=True 이면 검증 로직으로 오탐을 거릅니다."""
import re
from datetime import date

PATTERNS = {
    "RRN": re.compile(r"(?<!\d)\d{6}-?[1-4]\d{6}(?!\d)"),
    "PHONE": re.compile(r"(?<!\d)(?:\+82[-\s]?10|010)[-\s]?\d{4}[-\s]?\d{4}(?!\d)"),
    "EMAIL": re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),
    "BRN": re.compile(r"(?<!\d)\d{3}-\d{2}-\d{5}(?!\d)"),
    "CARD": re.compile(r"(?<!\d)(?:\d{4}[- ]?){3}\d{4}(?!\d)"),
}


def digits(s):
    return re.sub(r"\D", "", s)


def rrn_ok(s):
    d = digits(s)
    year = int(d[:2]) + (1900 if d[6] in "12" else 2000)
    try:
        date(year, int(d[2:4]), int(d[4:6]))           # 실제 달력에 있는 생년월일인지
    except ValueError:
        return False
    w = [2, 3, 4, 5, 6, 7, 8, 9, 2, 3, 4, 5]
    total = sum(int(c) * k for c, k in zip(d[:12], w))
    return (11 - total % 11) % 10 == int(d[12])        # 검증 숫자


def brn_ok(s):
    d = [int(c) for c in digits(s)]
    w = [1, 3, 7, 1, 3, 7, 1, 3, 5]
    total = sum(a * b for a, b in zip(d[:9], w)) + (d[8] * 5) // 10
    return (10 - total % 10) % 10 == d[9]


def luhn_ok(s):
    total = 0
    for i, c in enumerate(reversed(digits(s))):
        n = int(c) * (2 if i % 2 else 1)
        total += n - 9 if n > 9 else n
    return total % 10 == 0


CHECKS = {"RRN": rrn_ok, "BRN": brn_ok, "CARD": luhn_ok}


def scan_text(text, validate):
    found = []
    for kind, rx in PATTERNS.items():
        for m in rx.finditer(text):
            if validate and kind in CHECKS and not CHECKS[kind](m.group()):
                continue
            found.append({"type": kind, "start": m.start(), "end": m.end(), "score": 1.0})
    return found
