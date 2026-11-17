#!/usr/bin/env python3
# 사용: python spf_count.py
# SPF 는 평가 중 DNS 조회가 10번을 넘으면 permerror 가 된다(RFC 7208 4.6.4).
# 조회로 세는 항목: include, a, mx, ptr, exists, redirect. ip4, ip6, all 은 세지 않는다.
# 이 스크립트는 DNS 에 접속하지 않고, 아래 시험용 레코드 표만 읽는다.
RECORDS = {
    "example.com": "v=spf1 include:mail.example.net include:crm.example.org a mx -all",
    "mail.example.net": "v=spf1 include:_spf.example.net ip4:203.0.113.0/24 -all",
    "_spf.example.net": "v=spf1 include:s1.example.net include:s2.example.net include:s3.example.net ~all",
    "s1.example.net": "v=spf1 ip4:198.51.100.0/25 -all",
    "s2.example.net": "v=spf1 a mx -all",
    "s3.example.net": "v=spf1 ip4:198.51.100.128/25 -all",
    "crm.example.org": "v=spf1 include:bulk.example.org mx -all",
    "bulk.example.org": "v=spf1 a:send.example.org ip4:192.0.2.0/24 -all",
}
COUNTED = ("include:", "a", "a:", "mx", "mx:", "ptr", "exists:", "redirect=")


def counts(term):
    return any(term == c or term.startswith(c) for c in COUNTED if c.endswith((":", "=")) or term == c)


def walk(domain, depth=0):
    total = 0
    for term in RECORDS[domain].split()[1:]:
        name = term.lstrip("+-~?")
        if not counts(name):
            continue
        total += 1
        print("  " * depth + f"{domain}: {name}")
        if name.startswith("include:"):
            total += walk(name.split(":", 1)[1], depth + 1)
    return total


n = walk("example.com")
print()
print(f"DNS 조회 {n}회, 한도 10회")
print("판정: " + ("permerror 위험" if n > 10 else "한도 이내"))
