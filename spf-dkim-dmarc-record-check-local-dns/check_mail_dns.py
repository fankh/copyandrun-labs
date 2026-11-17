"""SPF, DKIM, DMARC 기록을 DNS 에서 읽어 문법을 점검하는 스크립트입니다.

사용법: python3 check_mail_dns.py 도메인 [--selector 선택자 ...] [--from 보낸사람도메인] [--server 127.0.0.1]
- SPF: v=spf1 문법, 기록 개수, DNS 조회 횟수(10회 제한), all 한정자 요약
- DKIM: 선택자별 공개키 TXT 의 태그, base64, RSA 키 길이
- DMARC: 정책 요약(p, sp, pct, rua, 정렬 방식), --from 을 주면 정렬 판정(둘 다 실패하면 오류)
"""
import argparse
import base64
import binascii
import ipaddress
import re
import sys

import dns.exception
import dns.resolver

TERM = re.compile(r"^([+\-~?])?(all|include|a|mx|ptr|ip4|ip6|exists)(?:[:/=](.*))?$|^(redirect|exp)=(.+)$", re.I)
RESOLVER = dns.resolver.Resolver(configure=False)


def txt(name):
    """이름의 TXT 기록을 문자열 목록으로 돌려줍니다. 255바이트씩 나뉜 조각은 공백 없이 이어 붙입니다."""
    try:
        ans = RESOLVER.resolve(name, "TXT")
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
        return []
    return ["".join(s.decode() for s in r.strings) for r in ans]


def exists(name, rtype):
    try:
        RESOLVER.resolve(name, rtype)
        return True
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
        return False


# ---------------------------------------------------------------- SPF
def spf_walk(domain, state, depth=0):
    """SPF 기록을 따라가며 DNS 조회 횟수를 세고 문제를 모읍니다."""
    pad = "  " * depth
    recs = [t for t in txt(domain) if t.lower().startswith("v=spf1")]
    if not recs:
        state["errors"].append(f"{domain}: SPF 기록이 없습니다")
        return
    if len(recs) > 1:
        state["errors"].append(f"{domain}: SPF 기록이 {len(recs)}개입니다 (permerror)")
        return
    rec = recs[0]
    print(f"{pad}{domain}: {rec}")
    terms = rec.split()[1:]
    seen_all = False
    for t in terms:
        m = TERM.match(t)
        if not m:
            state["errors"].append(f"{domain}: 알 수 없는 항목 '{t}'")
            continue
        qual, mech, arg = m.group(1), (m.group(2) or m.group(4)).lower(), m.group(3) or m.group(5)
        if seen_all:
            state["warns"].append(f"{domain}: all 뒤의 '{t}' 는 평가되지 않습니다")
            continue
        if mech in ("ip4", "ip6"):
            try:
                net = ipaddress.ip_network(arg, strict=False)
                if net.version != (4 if mech == "ip4" else 6):
                    raise ValueError
            except ValueError:
                state["errors"].append(f"{domain}: '{t}' 의 주소 또는 접두어 길이가 잘못됐습니다")
        elif mech == "all":
            seen_all = True
            state["all"] = (qual or "+") + "all"
        elif mech in ("include", "a", "mx", "ptr", "exists", "redirect"):
            state["lookups"] += 1
            if mech in ("include", "redirect"):
                if not arg:
                    state["errors"].append(f"{domain}: '{t}' 에 도메인이 없습니다")
                elif depth < 12:
                    spf_walk(arg, state, depth + 1)
            elif mech in ("a", "mx"):
                target = arg.split("/")[0] if arg and not arg.startswith("/") else domain
                if not exists(target, "A" if mech == "a" else "MX"):
                    state["voids"] += 1


def check_spf(domain):
    print("[SPF]")
    state = {"lookups": 0, "voids": 0, "errors": [], "warns": [], "all": None}
    spf_walk(domain, state)
    if state["lookups"] > 10:
        state["errors"].append(f"DNS 조회 {state['lookups']}회로 10회 제한을 넘습니다 (RFC 7208 4.6.4, permerror)")
    if state["voids"] > 2:
        state["warns"].append(f"빈 응답 조회가 {state['voids']}회입니다 (void lookup 2회 권고 초과)")
    if state["all"] == "+all":
        state["warns"].append("+all 은 모든 서버를 허용합니다")
    elif state["all"] == "?all":
        state["warns"].append("?all 은 판정을 하지 않겠다는 뜻입니다")
    elif state["all"] is None and not state["errors"]:
        state["warns"].append("끝맺는 all 또는 redirect 가 없습니다")
    print(f"조회 횟수 {state['lookups']}회 / 끝맺음 {state['all']}")
    report(state)


# ---------------------------------------------------------------- DKIM
def der(b, i):
    """DER 항목 하나를 읽어 (태그, 내용 시작, 내용 끝)을 돌려줍니다."""
    tag, ln = b[i], b[i + 1]
    j = i + 2
    if ln & 0x80:
        n = ln & 0x7F
        ln = int.from_bytes(b[j:j + n], "big")
        j += n
    return tag, j, j + ln


def rsa_bits(blob):
    """SubjectPublicKeyInfo 에서 RSA 모듈러스의 비트 수를 구합니다."""
    _, s, _ = der(blob, 0)                  # SEQUENCE
    _, _, e = der(blob, s)                  # AlgorithmIdentifier 건너뜀
    tag, s2, _ = der(blob, e)               # BIT STRING
    if tag != 0x03:
        raise ValueError("공개키 구조가 아닙니다")
    inner = blob[s2 + 1:]                   # 미사용 비트 수 1바이트 건너뜀
    _, s3, _ = der(inner, 0)                # RSAPublicKey SEQUENCE
    tag, s4, e4 = der(inner, s3)            # modulus INTEGER
    if tag != 0x02:
        raise ValueError("RSA 모듈러스를 찾지 못했습니다")
    return int.from_bytes(inner[s4:e4], "big").bit_length()


def parse_tags(text):
    tags, order = {}, []
    for part in text.split(";"):
        if "=" in part:
            k, v = part.split("=", 1)
            k = k.strip()
            tags.setdefault(k, v.strip())
            order.append(k)
    return tags, order


def check_dkim(domain, selector):
    name = f"{selector}._domainkey.{domain}"
    print(f"[DKIM] {name}")
    state = {"errors": [], "warns": []}
    recs = txt(name)
    if not recs:
        state["errors"].append("선택자 기록이 없습니다")
        return report(state)
    if len(recs) > 1:
        state["errors"].append(f"TXT 가 {len(recs)}개입니다")
    tags, order = parse_tags(recs[0])
    if "v" in tags and (order[0] != "v" or tags["v"] != "DKIM1"):
        state["errors"].append("v 태그는 첫 태그이고 값은 DKIM1 이어야 합니다")
    k = tags.get("k", "rsa")
    flags = [x.strip() for x in tags.get("t", "").split(":") if x.strip()]
    if "p" not in tags:
        state["errors"].append("p 태그(공개키)가 없습니다")
    elif tags["p"] == "":
        state["errors"].append("p 가 비어 있어 폐기된 키입니다 (RFC 6376 3.6.1)")
    else:
        try:
            raw = base64.b64decode(tags["p"].replace(" ", ""), validate=True)
            if k == "rsa":
                bits = rsa_bits(raw)
                print(f"키 종류 rsa / 길이 {bits}비트")
                if bits < 1024:
                    state["warns"].append("1024비트 미만입니다")
            else:
                print(f"키 종류 {k} / 공개키 {len(raw)}바이트")
        except binascii.Error:
            state["errors"].append("p 값이 올바른 base64 가 아닙니다")
        except (ValueError, IndexError):
            state["errors"].append("p 값이 공개키 구조(SubjectPublicKeyInfo)가 아닙니다")
    if "y" in flags:
        state["warns"].append("t=y: 테스트 중인 키라 검증 실패를 엄격히 다루지 않을 수 있습니다")
    report(state)


# ---------------------------------------------------------------- DMARC
def aligned(from_domain, auth_domain, mode):
    """정렬 판정입니다. 공개 접미사 목록 없이, 한쪽이 다른 쪽과 같거나 하위 도메인이면 같은 조직으로 보는 단순화입니다."""
    if mode == "s":
        return from_domain == auth_domain
    return (from_domain == auth_domain
            or from_domain.endswith("." + auth_domain)
            or auth_domain.endswith("." + from_domain))


def check_dmarc(domain, from_domain):
    name = f"_dmarc.{domain}"
    print(f"[DMARC] {name}")
    state = {"errors": [], "warns": []}
    recs = [t for t in txt(name) if t.lower().startswith("v=dmarc1")]
    if not recs:
        state["warns"].append("DMARC 기록이 없습니다")
        return report(state)
    if len(recs) > 1:
        state["errors"].append(f"DMARC 기록이 {len(recs)}개입니다")
    tags, order = parse_tags(recs[0])
    if order[:2] != ["v", "p"]:
        state["errors"].append("v, p 순서로 시작해야 합니다 (RFC 7489 6.3)")
    p = tags.get("p", "")
    if p not in ("none", "quarantine", "reject"):
        state["errors"].append(f"p={p or '(없음)'} 는 허용 값(none, quarantine, reject)이 아닙니다")
    sp = tags.get("sp", p)
    if "sp" in tags and sp not in ("none", "quarantine", "reject"):
        state["errors"].append(f"sp={sp} 는 허용 값이 아닙니다")
    try:
        pct = int(tags.get("pct", "100"))
        if not 0 <= pct <= 100:
            raise ValueError
    except ValueError:
        pct = None
        state["errors"].append(f"pct={tags.get('pct')} 는 0~100 정수가 아닙니다")
    rua = [x.strip() for x in tags.get("rua", "").split(",") if x.strip()]
    for u in rua:
        if not u.lower().startswith("mailto:"):
            state["errors"].append(f"rua '{u}' 는 mailto: 로 시작해야 합니다")
    adkim, aspf = tags.get("adkim", "r"), tags.get("aspf", "r")
    print(f"정책 p={p} / 하위 도메인 sp={sp} / 적용 비율 pct={pct if pct is not None else '?'}")
    print(f"정렬 DKIM={'엄격' if adkim == 's' else '느슨'} SPF={'엄격' if aspf == 's' else '느슨'} / 보고서 수신 {len(rua)}곳")
    if p == "none":
        state["warns"].append("p=none 은 관찰만 하고 막지 않습니다")
    if pct is not None and pct < 100 and p != "none":
        state["warns"].append(f"정책이 메일의 {pct}% 에만 적용됩니다")
    if not rua:
        state["warns"].append("rua 가 없어 집계 보고서를 받을 수 없습니다")
    if from_domain:
        dk_ok = aligned(from_domain, domain, adkim)
        spf_ok = aligned(from_domain, domain, aspf)
        print(f"From {from_domain}: DKIM 정렬 {'통과' if dk_ok else '실패'}, SPF 정렬 {'통과' if spf_ok else '실패'}")
        if not (dk_ok or spf_ok):
            state["errors"].append(f"From {from_domain} 은 DKIM, SPF 정렬이 모두 실패해 DMARC 가 실패합니다 "
                                   f"(RFC 7489 3.1, p={p} 대상)")
    report(state)


def report(state):
    for e in state["errors"]:
        print(f"  오류: {e}")
    for w in state["warns"]:
        print(f"  주의: {w}")
    if not state["errors"] and not state["warns"]:
        print("  문제 없음")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("domain")
    ap.add_argument("--selector", action="append", default=None)
    ap.add_argument("--from", dest="from_domain")
    ap.add_argument("--server", default="127.0.0.1")
    a = ap.parse_args()
    RESOLVER.nameservers = [a.server]
    RESOLVER.lifetime = 5
    print(f"== {a.domain} ==")
    check_spf(a.domain)
    for sel in a.selector or ["s2026"]:
        check_dkim(a.domain, sel)
    check_dmarc(a.domain, a.from_domain)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
