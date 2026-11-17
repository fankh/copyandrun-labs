"""연습용 시험 메일 3개를 samples 폴더에 만듭니다.

도메인은 예약 도메인(example.com, example.test 등)과 문서용 IP(192.0.2.x, 203.0.113.x)만 씁니다.
Authentication-Results 는 이 글에서 직접 써 넣은 값이며, 실제 서버가 검사한 결과가 아닙니다.
"""
from datetime import datetime, timedelta, timezone
from email.message import EmailMessage
from email.headerregistry import Address
from email.utils import format_datetime
from pathlib import Path

BASE = datetime(2026, 11, 2, 9, 0, 0, tzinfo=timezone.utc)


def received(hops):
    """hops 는 오래된 것부터. 실제 메일처럼 가장 새로운 Received 가 위로 오게 뒤집어 돌려줍니다."""
    lines = []
    for n, (src_host, src_ip, by_host, minutes) in enumerate(hops, start=1):
        when = format_datetime(BASE + timedelta(minutes=minutes))
        lines.append(f"from {src_host} ({src_host} [{src_ip}]) by {by_host} with ESMTPS id h{n}; {when}")
    return list(reversed(lines))


def build(name, sender, return_path, reply_to, auth, hops, text, html):
    msg = EmailMessage()
    msg["Return-Path"] = f"<{return_path}>"
    for line in received(hops):
        msg["Received"] = line
    if auth:
        msg["Authentication-Results"] = auth
    msg["From"] = sender
    msg["To"] = Address("받는 사람", "reader", "example.com")
    if reply_to:
        msg["Reply-To"] = reply_to
    msg["Subject"] = name[0]
    msg["Date"] = format_datetime(BASE + timedelta(minutes=hops[-1][3] + 1))
    msg["Message-ID"] = f"<{name[1]}-0001@{sender.domain}>"
    msg.set_content(text)
    msg.add_alternative(html, subtype="html")
    return msg


def main():
    out = Path("samples")
    out.mkdir(exist_ok=True)

    ok = build(
        ("11월 소식지", "ok"),
        Address("Example 소식", "news", "example.com"),
        Address("", "bounce-news", "example.com"),
        None,
        "mx.example.com; spf=pass smtp.mailfrom=example.com; dkim=pass header.d=example.com; dmarc=pass header.from=example.com",
        [("app01.example.com", "192.0.2.10", "relay.example.com", 0),
         ("relay.example.com", "192.0.2.20", "mx.example.com", 1)],
        "11월 소식지입니다. https://www.example.com/news",
        '<p>11월 소식지입니다. <a href="https://www.example.com/news">소식 보기</a></p>',
    )

    spoof = build(
        ("계정 보안 확인 요청", "spoof"),
        Address("ExamplePay 보안팀", "security", "mail-notice.example.test"),
        Address("", "bounce", "bulk-sender.example.net"),
        Address("", "helpdesk", "free-mail.example.org"),
        "mx.example.com; spf=fail smtp.mailfrom=bulk-sender.example.net; dkim=none; dmarc=fail header.from=mail-notice.example.test",
        [("unknown", "203.0.113.45", "bulk-relay.example.net", 5),
         ("bulk-relay.example.net", "203.0.113.46", "edge.example.net", 3),
         ("edge.example.net", "203.0.113.47", "mx.example.com", 6)],
        "계정이 잠길 수 있습니다. 회신 주소로 연락해 주세요.",
        "<p>계정이 잠길 수 있습니다. 회신 주소로 연락해 주세요.</p>",
    )

    link = build(
        ("결제 내역 확인", "link"),
        Address("Example 결제", "billing", "example.com"),
        Address("", "bounce-billing", "example.com"),
        None,
        "mx.example.com; spf=pass smtp.mailfrom=example.com; dkim=pass header.d=example.com; dmarc=pass header.from=example.com",
        [("app01.example.com", "192.0.2.10", "relay.example.com", 0),
         ("relay.example.com", "192.0.2.20", "mx.example.com", 1)],
        "결제 내역을 확인해 주세요. hxxp://login-check.example.test/verify",
        '<p>결제 내역을 확인해 주세요.</p>'
        '<p><a href="http://login-check.example.test/verify?u=1">https://www.example.com/account</a></p>'
        '<p><a href="http://login-check.example.test/help">여기를 눌러 확인</a></p>',
    )

    for fname, msg in (("ok", ok), ("spoof", spoof), ("link", link)):
        (out / f"{fname}.eml").write_bytes(msg.as_bytes())
        print("만든 파일:", out / f"{fname}.eml")


if __name__ == "__main__":
    main()
