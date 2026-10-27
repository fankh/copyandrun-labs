"""마스킹 규칙 점검: 가려야 할 것은 가리고, 가리면 안 되는 것은 그대로 두는지 확인합니다."""
from pii import luhn_ok, mask_text

DOMAIN = "example.com"

CASES = [
    # (입력, 로그 스타일 기대값)
    ("rrn=900101-1234567", "rrn=******-*******"),
    ("rrn=9001011234567", "rrn=******-*******"),
    ("rrn=901301-1234567", "rrn=901301-1234567"),  # 13월은 날짜가 아닙니다
    ("주문 ORD-2610271234567", "주문 ORD-2610271234567"),  # 앞에 붙은 접두어가 있으면 건드리지 않습니다
    ("tel=010-1234-5678", "tel=010-****-5678"),
    ("tel=01012345678", "tel=010****5678"),
    (f"mail=tester1@{DOMAIN}", f"mail=t***@{DOMAIN}"),
    ("card=4111 1111 1111 1111", "card=**** **** **** 1111"),
    ("card=5555-5555-5555-4444", "card=****-****-****-4444"),
    ("track=1234-5678-9012-3456", "track=1234-5678-9012-3456"),  # Luhn 불일치
]

for text, want in CASES:
    got = mask_text(text)
    assert got == want, f"{text!r}\n  기대 {want!r}\n  결과 {got!r}"

prompt = mask_text("연락처 010-1234-5678, 주민번호 900101-1234567", style="prompt")
assert prompt == "연락처 [전화번호], 주민번호 [주민번호]", prompt
assert luhn_ok("4111111111111111") and not luhn_ok("1234567890123456")
print(f"마스킹 규칙 점검 통과 ({len(CASES) + 2}건)")
