"""시험용 가짜 개인정보 파일과 정답표(labels.json)를 만듭니다. 실제 사람의 정보는 없습니다.

주민등록번호 형식 값은 생년월일과 검증 숫자 규칙만 맞춘 임의 번호입니다.
앞 6자리와 뒤 7자리를 따로 조합해 만들며, 이 스크립트의 출력에는 그대로 찍지 않습니다.
"""
import json
import random
from pathlib import Path

rnd = random.Random(20261102)
AT = "@"                       # 이메일 주소를 소스에 그대로 쓰지 않으려고 따로 둡니다
OUT = Path("data")


def rrn_check(first12):
    w = [2, 3, 4, 5, 6, 7, 8, 9, 2, 3, 4, 5]
    s = sum(int(c) * k for c, k in zip(first12, w))
    return str((11 - s % 11) % 10)


def make_rrn(birth6, gender, valid=True):
    tail6 = "".join(str(rnd.randint(0, 9)) for _ in range(5))
    first12 = (birth6 + str(gender) + tail6)[:12]
    check = rrn_check(first12)
    if not valid:                                       # 검증 숫자를 일부러 틀리게 만든 값
        check = str((int(check) + 3) % 10)
    return birth6, first12[6:] + check


def luhn_ok(num):
    total = 0
    for i, c in enumerate(reversed(num)):
        d = int(c)
        if i % 2 == 1:
            d = d * 2 - 9 if d * 2 > 9 else d * 2
        total += d
    return total % 10 == 0


def make_card(prefix):
    while True:
        body = prefix + "".join(str(rnd.randint(0, 9)) for _ in range(15 - len(prefix)))
        for chk in range(10):
            if luhn_ok(body + str(chk)):
                return body + str(chk)


def not_luhn_16():
    while True:
        n = "".join(str(rnd.randint(0, 9)) for _ in range(16))
        if not luhn_ok(n):
            return n


def make_brn(valid=True):
    d = [rnd.randint(1, 9) for _ in range(3)] + [rnd.randint(1, 9) for _ in range(2)] + [rnd.randint(0, 9) for _ in range(4)]
    w = [1, 3, 7, 1, 3, 7, 1, 3, 5]
    s = sum(a * b for a, b in zip(d, w)) + (d[8] * 5) // 10
    chk = (10 - s % 10) % 10
    if not valid:
        chk = (chk + 4) % 10
    t = "".join(map(str, d)) + str(chk)
    return f"{t[:3]}-{t[3:5]}-{t[5:]}"


truth = []     # {file, type, text}
files = {}


def put(name, text, kind=None, value=None):
    files.setdefault(name, []).append(text)
    if kind:
        truth.append({"file": name, "type": kind, "text": value})


def phone(mid="5550"):
    return f"{mid}-{rnd.randint(0, 9999):04d}"


# ---- customers.csv: 정상 서식 위주 ----
csv_rows = ["이름,연락처,이메일,주민등록번호,사업자등록번호,메모"]
births = ["900101", "851130", "010315", "770622", "030228", "950909"]
for i, b in enumerate(births, 1):
    g = 1 if int(b[:2]) > 25 else 3
    g = g + (i % 2)                                     # 1/2 또는 3/4
    front, back = make_rrn(b, g)
    rrn = f"{front}-{back}"
    ph = "010-" + phone()
    em = f"test{i:02d}" + AT + "example.com"
    csv_rows.append(f"시험고객{i:02d},{ph},{em},{rrn},,")
    truth += [{"file": "customers.csv", "type": t, "text": v} for t, v in
              (("PHONE", ph), ("EMAIL", em), ("RRN", rrn))]
files["customers.csv"] = csv_rows

# ---- memo.txt: 자유 문장 속 여러 서식, 놓치기 쉬운 표기 포함 ----
def t(kind, v):
    truth.append({"file": "memo.txt", "type": kind, "text": v})
    return v

f, b = make_rrn("880808", 1)
no_hyphen = f + b
f2, b2 = make_rrn("991231", 2)
spaced = f"{f2} {b2}"
f3, b3 = make_rrn("050505", 3, valid=True)
new_style = f"{f3}-{b3[:-1]}{(int(b3[-1]) + 3) % 10}"  # 2020년 10월 이후 발급처럼 검증 숫자가 맞지 않는 값
brn = [make_brn() for _ in range(3)]
cards = [make_card("4"), make_card("51"), make_card("35")]
lines = [
    "상담 메모 (시험용 가짜 데이터)",
    f"고객이 구두로 알려 준 번호는 {t('RRN', no_hyphen)} 이고 하이픈 없이 적었음.",
    f"다른 고객은 {spaced} 처럼 공백으로 적음.",
    f"신규 발급 형식이라는 {t('RRN', new_style)} 도 접수됨.",
    f"휴대전화는 {t('PHONE', '01055501234')} 또는 {t('PHONE', '+82 10-5550-2345')}.",
    f"다른 표기: {t('PHONE', '010 5550 3456')} 와 공일공-오오오공-사오육칠.",
    f"이메일 {t('EMAIL', 'memo01' + AT + 'example.com')} 로 회신, 또는 memo02 at example dot com 으로 보내 달라고 함.",
    f"사업자등록번호 {t('BRN', brn[0])}, {t('BRN', brn[1])}, {t('BRN', brn[2])}.",
    f"결제 카드 {t('CARD', cards[0][:4] + '-' + cards[0][4:8] + '-' + cards[0][8:12] + '-' + cards[0][12:])}, "
    f"{t('CARD', cards[1][:4] + ' ' + cards[1][4:8] + ' ' + cards[1][8:12] + ' ' + cards[1][12:])}, {t('CARD', cards[2])}.",
]
files["memo.txt"] = lines
truth += [{"file": "memo.txt", "type": "RRN", "text": spaced},
          {"file": "memo.txt", "type": "PHONE", "text": "공일공-오오오공-사오육칠"},
          {"file": "memo.txt", "type": "EMAIL", "text": "memo02 at example dot com"}]

# ---- orders.txt: 개인정보가 아닌데 모양이 비슷한 값(오탐 유도) ----
orders = ["주문 내역 (개인정보 없음, 시험용)"]
for i in range(3):
    # 생년월일처럼 보이는 앞 6자리 + 성별 자리 1~4 + 검증 숫자가 틀린 뒤 7자리
    front = f"26{rnd.randint(1, 12):02d}{rnd.randint(1, 28):02d}"
    _, back = make_rrn(front, rnd.randint(1, 4), valid=False)
    orders.append(f"주문번호 {front}-{back} 배송 완료")
orders.append(f"송장번호 {make_rrn('261102', 2, valid=False)[0]}{make_rrn('261102', 2, valid=False)[1]} 출고")
for i in range(2):
    n = not_luhn_16()
    orders.append(f"주문 묶음 번호 {n[:4]}-{n[4:8]}-{n[8:12]}-{n[12:]} 접수")
orders.append(f"상품 코드 {make_brn(valid=False)} 재고 확인")
orders.append("일시 2026-11-02 14:30, 문의 대표번호 02-555-0100, 버전 3.12 는 개인정보가 아님")
files["orders.txt"] = orders

OUT.mkdir(exist_ok=True)
for name, rows in files.items():
    (OUT / name).write_text("\n".join(rows) + "\n", encoding="utf-8", newline="\n")


for item in truth:
    text = (OUT / item["file"]).read_text(encoding="utf-8")
    s = text.find(item["text"])
    assert s >= 0, item
    item["start"], item["end"] = s, s + len(item["text"])
(OUT / "labels.json").write_text(json.dumps(truth, ensure_ascii=False, indent=1), encoding="utf-8")
print("만든 파일:", ", ".join(sorted(files)), "/ 정답표", len(truth), "건")
