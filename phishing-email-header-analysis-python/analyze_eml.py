"""의심 메일(.eml)의 헤더와 링크에서 확인할 항목을 하나씩 나열합니다. 점수는 매기지 않습니다.

사용법: python analyze_eml.py 메일.eml [--brand 단어] [--trusted-id 서버이름]
표준 라이브러리만 씁니다. 표시는 점검을 돕는 용도이며, 결론은 사람이 내립니다.
"""
import argparse
import re
from email import policy
from email.parser import BytesParser
from email.utils import getaddresses, parsedate_to_datetime
from html.parser import HTMLParser
from urllib.parse import urlsplit

OK, WARN, NA = "정상", "주의", "확인 불가"


def domain_of(address):
    return address.rpartition("@")[2].lower()


def related(a, b):
    """같거나 한쪽이 다른 쪽의 하위 도메인이면 관련 있다고 봅니다(공개 접미사 목록은 쓰지 않습니다)."""
    return a == b or a.endswith("." + b) or b.endswith("." + a)


def defang(url):
    return re.sub(r"^http", "hxxp", url, flags=re.I)


def from_parts(msg):
    out = []
    for header in msg.get_all("From", []):
        for name, addr in getaddresses([str(header)]):
            out.append((name, domain_of(addr)))
    return out


def check_received(msg):
    hops = []
    for value in reversed(msg.get_all("Received", [])):  # 아래쪽이 먼저 거친 서버입니다
        text = " ".join(str(value).split())
        src = re.search(r"\bfrom\s+(\S+)", text)
        by = re.search(r"\bby\s+(\S+)", text)
        ip = re.search(r"\[([0-9A-Fa-f:.]+)\]", text)
        when = None
        if ";" in text:
            try:
                when = parsedate_to_datetime(text.rsplit(";", 1)[1].strip())
            except (TypeError, ValueError):
                pass
        hops.append((src.group(1) if src else "?", ip.group(1) if ip else "?", by.group(1) if by else "?", when))
    if not hops:
        return NA, ["Received 헤더가 없습니다"]
    details, status = [], OK
    for n, (src, ip, by, when) in enumerate(hops, start=1):
        stamp = when.strftime("%H:%M:%S") if when else "시각 없음"
        details.append(f"{n}. {src} [{ip}] -> {by}  {stamp}")
    for n in range(1, len(hops)):
        a, b = hops[n - 1][3], hops[n][3]
        if a and b and b < a:
            status = WARN
            details.append(f"{n}번과 {n + 1}번 사이에 시각이 거꾸로 갑니다(서버 시계 차이이거나 꾸며 넣은 줄일 수 있음)")
    if hops[0][0] == "unknown":
        status = WARN
        details.append("첫 번째 경유 서버의 이름이 unknown 입니다")
    return status, details


def check_return_path(msg, from_domains):
    rp = msg.get("Return-Path")
    if not rp or not from_domains:
        return NA, ["Return-Path 또는 From 이 없습니다"]
    rp_domain = domain_of(getaddresses([str(rp)])[0][1])
    details = [f"Return-Path 도메인 {rp_domain}", f"From 도메인 {', '.join(from_domains)}"]
    if all(related(rp_domain, d) for d in from_domains):
        return OK, details
    return WARN, details + ["두 도메인이 서로 관련 없습니다(메일링 서비스를 쓰는 정상 메일도 이럴 수 있음)"]


def check_reply_to(msg, from_domains):
    values = msg.get_all("Reply-To", [])
    if not values:
        return OK, ["Reply-To 가 없습니다. 답장은 From 으로 갑니다"]
    domains = [domain_of(a) for _, a in getaddresses([str(v) for v in values])]
    details = [f"Reply-To 도메인 {', '.join(domains)}", f"From 도메인 {', '.join(from_domains)}"]
    if all(related(d, f) for d in domains for f in from_domains):
        return OK, details
    return WARN, details + ["답장이 From 과 다른 도메인으로 갑니다"]


def check_auth(msg, trusted_id):
    details, bad, seen = [], False, 0
    for value in msg.get_all("Authentication-Results", []):
        text = " ".join(str(value).split())
        server = text.split(";", 1)[0].strip()
        if trusted_id and server != trusted_id:
            details.append(f"무시: authserv-id {server} (신뢰하는 서버가 아님)")
            continue
        for method, result in re.findall(r"\b(spf|dkim|dmarc)=(\w+)", text):
            seen += 1
            details.append(f"{server}: {method}={result}")
            bad = bad or result != "pass"
    if not seen:
        return NA, details + ["확인할 Authentication-Results 가 없습니다"]
    if not trusted_id:
        details.append("위조된 헤더일 수 있어 서버 신뢰를 확인하지 못했습니다(--trusted-id 로 내 메일 서버 이름을 지정하세요)")
    return (WARN if bad else OK), details


def check_display_name(msg, brands):
    parts = from_parts(msg)
    details, status = [], OK
    for name, domain in parts:
        if not name:
            details.append(f"표시 이름 없음, From 도메인 {domain}")
            continue
        details.append(f"표시 이름 '{name}', From 도메인 {domain}")
        for token in re.findall(r"[\w-]+(?:\.[\w-]+)+", name):
            if not related(token.lower(), domain):
                status = WARN
                details.append(f"표시 이름 안의 {token} 이 실제 From 도메인과 다릅니다")
        squeezed = re.sub(r"[\s_-]", "", name).lower()
        for word in brands:
            if word.lower() in squeezed and word.lower() not in domain.replace("-", ""):
                status = WARN
                details.append(f"표시 이름에 {word} 가 있지만 From 도메인에는 없습니다")
    return (status if parts else NA), details or ["From 이 없습니다"]


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self._href, self._text = [], None, []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self._href, self._text = dict(attrs).get("href", ""), []

    def handle_data(self, data):
        if self._href is not None:
            self._text.append(data)

    def handle_endtag(self, tag):
        if tag == "a" and self._href is not None:
            self.links.append((" ".join("".join(self._text).split()), self._href))
            self._href = None


def check_links(msg):
    parser = Links()
    for part in msg.walk():
        if part.get_content_type() == "text/html":
            parser.feed(part.get_content())
    if not parser.links:
        return NA, ["HTML 본문에 링크가 없습니다"]
    status, details = OK, []
    for text, href in parser.links:
        host = (urlsplit(href).hostname or "").lower()
        shown = re.fullmatch(r"(?:https?://)?([\w-]+(?:\.[\w-]+)+)(?:[/?#]\S*)?", text, re.I)
        details.append(f"표시 '{text}' -> 실제 {defang(href)}")
        if shown and not related(shown.group(1).lower(), host):
            status = WARN
            details.append(f"표시 텍스트의 도메인 {shown.group(1).lower()} 과 실제 도메인 {host} 이 다릅니다")
        elif not shown:
            details.append(f"표시 텍스트가 주소가 아니라 비교하지 못했습니다(실제 도메인 {host})")
    return status, details


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("eml")
    ap.add_argument("--brand", action="append", default=[], help="표시 이름에 쓰였는지 볼 이름(여러 번 지정 가능)")
    ap.add_argument("--trusted-id", help="내 메일 서버의 authserv-id. 지정하면 이 서버가 붙인 결과만 읽습니다")
    args = ap.parse_args()
    with open(args.eml, "rb") as f:
        msg = BytesParser(policy=policy.default).parse(f)
    from_domains = [d for _, d in from_parts(msg)]
    print(f"파일 {args.eml}  제목 {msg.get('Subject', '(없음)')}")
    checks = [
        ("Received 체인 (오래된 것부터)", check_received(msg)),
        ("Return-Path 와 From 도메인", check_return_path(msg, from_domains)),
        ("Reply-To 도메인", check_reply_to(msg, from_domains)),
        ("Authentication-Results", check_auth(msg, args.trusted_id)),
        ("표시 이름", check_display_name(msg, args.brand)),
        ("링크 표시 텍스트와 실제 주소", check_links(msg)),
    ]
    for title, (status, details) in checks:
        print(f"\n[{status}] {title}")
        for line in details:
            print(f"    {line}")


if __name__ == "__main__":
    main()
