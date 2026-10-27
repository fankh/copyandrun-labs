"""개인정보 마스킹: 정규식으로 후보를 찾고, 검증을 통과한 것만 가립니다."""
import logging
import re

# 주민등록번호 형식: 앞에 숫자, 영문, 하이픈이 붙은 긴 번호의 일부는 제외합니다
RRN = re.compile(r"(?<![\w-])(\d{2})(\d{2})(\d{2})-?([1-8])\d{6}(?!\d)")
# 카드번호 형식: 4자리 네 묶음, 구분자는 공백 또는 하이픈 중 하나로 통일되어 있어야 합니다
CARD = re.compile(r"(?<![\w-])(\d{4})([- ]?)(\d{4})\2(\d{4})\2(\d{4})(?!\d)")
# 휴대전화: 010, 011, 016, 017, 018, 019
PHONE = re.compile(r"(?<![\w-])(01[016789])([-. ]?)(\d{3,4})([-. ]?)(\d{4})(?!\d)")
EMAIL = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")

LABEL = {"rrn": "[주민번호]", "card": "[카드번호]", "phone": "[전화번호]", "email": "[이메일]"}


def luhn_ok(digits):
    """카드번호 체크섬(Luhn)입니다. 오른쪽에서 두 번째 자리부터 하나 걸러 두 배로 합니다."""
    total = 0
    for i, ch in enumerate(reversed(digits)):
        d = int(ch)
        if i % 2 == 1:
            d *= 2
            if d > 9:
                d -= 9
        total += d
    return total % 10 == 0


def mask_text(text, style="log"):
    """style="log" 는 일부를 남기는 마스킹, style="prompt" 는 종류만 알려 주는 표시로 바꿉니다."""
    prompt = style == "prompt"

    def card(m):
        digits = "".join(m.group(i) for i in (1, 3, 4, 5))
        if not luhn_ok(digits):
            return m.group(0)  # 체크섬이 틀리면 카드번호가 아니라 일련번호로 봅니다
        if prompt:
            return LABEL["card"]
        sep = m.group(2)
        return sep.join(["****", "****", "****", m.group(5)])

    def rrn(m):
        month, day = int(m.group(2)), int(m.group(3))
        if not (1 <= month <= 12 and 1 <= day <= 31):
            return m.group(0)  # 날짜가 될 수 없는 숫자는 건드리지 않습니다
        return LABEL["rrn"] if prompt else "******-*******"

    def phone(m):
        if prompt:
            return LABEL["phone"]
        return f"{m.group(1)}{m.group(2)}****{m.group(4)}{m.group(5)}"

    def email(m):
        if prompt:
            return LABEL["email"]
        local, domain = m.group(0).split("@", 1)
        return f"{local[0]}***@{domain}"

    text = CARD.sub(card, text)  # 카드를 먼저 처리해야 16자리 안의 13자리가 주민번호로 오인되지 않습니다
    text = RRN.sub(rrn, text)
    text = PHONE.sub(phone, text)
    return EMAIL.sub(email, text)


class PiiFilter(logging.Filter):
    """핸들러에 붙이는 필터입니다. 메시지와 예외 문구를 기록하기 직전에 마스킹합니다."""

    def filter(self, record):
        record.msg = mask_text(record.getMessage())
        record.args = ()
        if record.exc_info:
            text = logging.Formatter().formatException(record.exc_info)
            record.exc_text = mask_text(text)
        return True
