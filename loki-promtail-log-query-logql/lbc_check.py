#!/usr/bin/env python
"""Loki HTTP API 로 로그 저장 상태를 점검하고, 실패한 점검 개수를 종료 코드로 돌려준다.
사용: python lbc_check.py http://osk-lbc-loki-good:3100 --lines 38 --err5xx 5 --bf-ip 12"""
import json
import sys
import urllib.parse
import urllib.request

base = sys.argv[1]
arg = lambda k: int(sys.argv[sys.argv.index(k) + 1])
PAT = '| pattern `<ip> - <_> [<_>] "<_> <_> <_>" <status> <_> "<_>" "<_>"`'


def get(path, **q):
    url = f"{base}{path}?{urllib.parse.urlencode(q, doseq=True)}"
    return json.load(urllib.request.urlopen(url, timeout=20))


def instant(expr):
    r = get("/loki/api/v1/query", query=expr)["data"]["result"]
    return {tuple(sorted(x["metric"].items())): int(float(x["value"][1])) for x in r}


def count(expr):
    return sum(instant(f"sum(count_over_time({expr}[15m]))").values())


results = []
streams = len(get("/loki/api/v1/series", **{"match[]": '{job="nginx"}'})["data"])
results.append(("스트림 수 3 이하", streams <= 3, f"스트림 {streams}개"))
for name, needle in (("이메일", "@example.com"), ("토큰", "SECRETtok")):
    n = count(f'{{job="nginx"}} |= "{needle}"')
    results.append((f"원문 {name} 0건", n == 0, f"{n}건"))
n5 = count(f'{{job="nginx"}} {PAT} | status=~"5.."')
results.append(("5xx 개수 일치", n5 == arg("--err5xx"), f"Loki {n5} / 기대 {arg('--err5xx')}"))
total = count('{job="nginx"}')
results.append(("전체 줄 수 일치", total == arg("--lines"), f"Loki {total} / access.log {arg('--lines')}"))
bf = instant(f'sum by (ip) (count_over_time({{job="nginx"}} {PAT} | status="401" [15m]))')
top = max(bf.values()) if bf else 0
results.append(("401 최다 IP 탐지", top == arg("--bf-ip"), f"최다 {top}건 / 기대 {arg('--bf-ip')}"))
cfg = urllib.request.urlopen(base + "/config", timeout=20).read().decode()
ret = "retention_period: 1d" in cfg and "retention_enabled: true" in cfg   # /config 는 24h 를 1d 로 보여 준다
results.append(("보존 기간 설정", ret, "적용됨" if ret else "기본값"))

bad = 0
for name, ok, detail in results:
    print(f"  {'통과' if ok else '실패'}  {name:<16} {detail}")
    bad += not ok
print(f"  실패 {bad}개 -> 종료 코드 {bad}")
sys.exit(bad)
