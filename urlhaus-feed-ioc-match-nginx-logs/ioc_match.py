"""공개 IOC 피드(텍스트 목록)를 내려받아 nginx access 로그와 대조합니다.

사용법:
  python ioc_match.py --feed-file fake_iocs.txt --log access.log --allow allowlist.txt --trust-xff
  python ioc_match.py --feed-url "<피드 주소>" --cache feed_cache.txt --log access.log
  python ioc_match.py --feed-file fake_iocs.txt --log access.log --naive --trust-xff   (문자열 포함 검사, 비교용)

피드 주소에 인증 키가 들어갈 수 있으므로 주소는 출력하지 않고 호스트 이름만 보여 줍니다.
--trust-xff 는 X-Forwarded-For 값을 클라이언트 IP 로 취급하는 시험용 옵션이며 기본은 꺼져 있습니다.
이 값은 요청한 쪽이 마음대로 쓸 수 있으므로, 신뢰하는 프록시 뒤에서 남긴 로그에만 켭니다.
"""
import argparse
import ipaddress
import os
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from urllib.parse import urlsplit

MIN_INTERVAL = 300  # URLhaus API 문서가 안내한 덤프 최소 내려받기 간격(초)
LOG_LINE = re.compile(
    r'^(\S+) \[([^\]]+)\] "(\S+) (\S+) [^"]*" (\d+) "([^"]*)" "([^"]*)" xff="([^"]*)" host="([^"]*)"$'
)
UPDATED = re.compile(r"Last updated:\s*(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d)")


def fetch_feed(url, cache, min_interval=MIN_INTERVAL):
    """캐시가 충분히 새것이면 그대로 쓰고, 아니면 조건부 요청으로 내려받습니다."""
    host = urlsplit(url).hostname
    if os.path.exists(cache) and time.time() - os.path.getmtime(cache) < min_interval:
        print(f"[피드] {host}: 캐시 사용({min_interval}초 안에 받은 파일)")
        return open(cache, encoding="utf-8").read()
    req = urllib.request.Request(url, headers={"User-Agent": "ioc-match-lab/1.0"})
    if os.path.exists(cache):
        stamp = time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime(os.path.getmtime(cache)))
        req.add_header("If-Modified-Since", stamp)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            data = r.read().decode("utf-8", errors="replace")
        tmp = cache + ".tmp"
        with open(tmp, "w", encoding="utf-8", newline="\n") as f:
            f.write(data)
        os.replace(tmp, cache)
        print(f"[피드] {host}: 새로 받음({len(data)}글자)")
        return data
    except urllib.error.HTTPError as e:
        if e.code == 304 and os.path.exists(cache):
            os.utime(cache)
            print(f"[피드] {host}: 변경 없음(304), 캐시 사용")
            return open(cache, encoding="utf-8").read()
        raise SystemExit(f"[피드] {host}: HTTP {e.code} 로 받지 못했습니다")


def defang(s):
    return s.replace("http", "hxxp", 1).replace(".", "[.]")


def normalize(line):
    """한 줄을 (종류, 호스트, 경로)로 바꿉니다. 종류는 ip, domain, url 중 하나입니다."""
    s = line.strip()
    if not s or s.startswith("#"):
        return None
    if s.lower().startswith("hxxp"):
        s = "http" + s[4:]
    s = s.replace("[.]", ".")
    if "://" in s:
        p = urlsplit(s)
        host, path = (p.hostname or "").lower(), p.path or "/"
    elif "/" in s:
        host, _, rest = s.partition("/")
        host, path = host.lower(), "/" + rest
    else:
        host, path = s.lower(), ""
    if not host:
        return None
    try:
        ipaddress.ip_address(host)
        return ("ip" if not path else "url", host, path)
    except ValueError:
        pass
    return ("url" if path and path != "/" else "domain", host, path)


def load_iocs(text):
    seen, out = set(), []
    for line in text.splitlines():
        n = normalize(line)
        if n and n not in seen:
            seen.add(n)
            out.append(n)
    return out


def feed_age_hours(text):
    m = UPDATED.search(text)
    if not m:
        return None
    t = datetime.strptime(m.group(1), "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
    return (datetime.now(timezone.utc) - t).total_seconds() / 3600


def parse_log(path, trust_xff=False):
    for no, raw in enumerate(open(path, encoding="utf-8", errors="replace"), 1):
        m = LOG_LINE.match(raw.rstrip("\n"))
        if not m:
            continue
        addr, ts, method, uri, status, ref, ua, xff, host = m.groups()
        clients = [addr]
        if trust_xff:  # 시험용: 요청 헤더에 쓴 값이므로 신뢰하는 프록시가 붙인 경우에만 켭니다
            clients += [x.strip() for x in xff.split(",") if x.strip() and x.strip() != "-"]
        rp = urlsplit(ref) if ref not in ("", "-") else None
        yield {"no": no, "ts": ts, "uri": uri, "status": status, "raw": raw.rstrip("\n"),
               "clients": clients, "host": host.lower(),
               "ref_host": (rp.hostname or "").lower() if rp else "",
               "ref_path": (rp.path or "/") if rp else ""}


def host_match(obs, ioc_host):
    """도메인 경계를 지킵니다. evil.example.net 은 a.evil.example.net 과 일치하지만 notevil.example.net 과는 아닙니다."""
    return obs == ioc_host or obs.endswith("." + ioc_host)


def allowed(host, allow):
    return any(host_match(host, a) for a in allow)


def match(rec, iocs, allow):
    hits, skipped = [], []
    for kind, h, path in iocs:
        if kind == "ip":
            if h in rec["clients"]:
                hits.append(("경보", kind, h, "클라이언트 IP 일치"))
            continue
        for label, obs, obs_path in (("Referer", rec["ref_host"], rec["ref_path"]), ("Host", rec["host"], rec["uri"])):
            if not obs or not host_match(obs, h):
                continue
            if allowed(obs, allow):
                skipped.append((h, label))
            elif kind == "url" and not obs_path.startswith(path):
                hits.append(("확인", kind, h + path, f"{label} 호스트만 일치(경로 다름)"))
            else:
                hits.append(("경보", kind, h + path, f"{label} 일치"))
    return hits, skipped


def naive(rec, iocs):
    return [h for _, h, _ in iocs if h in rec["raw"]]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--feed-url")
    ap.add_argument("--feed-file")
    ap.add_argument("--cache", default="feed_cache.txt")
    ap.add_argument("--log", required=True)
    ap.add_argument("--allow")
    ap.add_argument("--max-age-hours", type=float, default=24)
    ap.add_argument("--naive", action="store_true")
    ap.add_argument("--trust-xff", action="store_true",
                    help="X-Forwarded-For 를 클라이언트 IP 로 취급합니다(기본 끔, 시험용)")
    a = ap.parse_args()

    if a.feed_url:
        text = fetch_feed(a.feed_url, a.cache)
    elif a.feed_file:
        text = open(a.feed_file, encoding="utf-8").read()
    else:
        sys.exit("--feed-url 또는 --feed-file 이 필요합니다")
    iocs = load_iocs(text)
    allow = []
    if a.allow:
        allow = [n[1] for n in map(normalize, open(a.allow, encoding="utf-8")) if n]
    age = feed_age_hours(text)
    kinds = {k: sum(1 for i in iocs if i[0] == k) for k in ("ip", "domain", "url")}
    print(f"[피드] IOC {len(iocs)}건 (ip {kinds['ip']}, domain {kinds['domain']}, url {kinds['url']}), 허용 목록 {len(allow)}건")
    if age is None:
        print("[피드] 갱신 시각 표시 없음")
    elif age > a.max_age_hours:
        print(f"[피드] 경고: 마지막 갱신이 {age / 24:.0f}일 전입니다. 오래된 목록으로는 최근 위협을 놓칩니다")
    else:
        print(f"[피드] 마지막 갱신 {age:.1f}시간 전")

    total = alerts = checks = skipped_n = 0
    for rec in parse_log(a.log, a.trust_xff):
        total += 1
        if a.naive:
            found = naive(rec, iocs)
            if found:
                alerts += 1
                print(f"줄 {rec['no']:>2} 포함 {rec['clients'][-1]:<11} IOC {','.join(defang(x) for x in found)}")
            continue
        hits, skipped = match(rec, iocs, allow)
        skipped_n += len(skipped)
        for level, kind, value, why in hits:
            alerts += level == "경보"
            checks += level == "확인"
            shown = value if kind == "ip" else defang(value)
            print(f"줄 {rec['no']:>2} {level} {rec['clients'][-1]:<11} {kind:<6} {shown:<30} {why}")
    print(f"[결과] 로그 {total}줄, 경보 {alerts}건, 확인 필요 {checks}건, 허용 목록으로 제외 {skipped_n}건")
    sys.exit(1 if alerts else 0)


if __name__ == "__main__":
    main()
