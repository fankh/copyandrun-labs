#!/usr/bin/env python
"""두 Loki 의 라벨 이름, uri 라벨 값 개수, 저장된 줄 예시를 보여 준다. 사용: python lbc_peek.py"""
import json
import sys
import time
import urllib.parse
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")


def get(base, path, **q):
    url = f"{base}{path}?{urllib.parse.urlencode(q)}"
    return json.load(urllib.request.urlopen(url, timeout=20))["data"]


for v in ("bad", "good"):
    base = f"http://osk-lbc-loki-{v}:3100"
    print(f"### {v}")
    print("  라벨 이름:", ", ".join(get(base, "/loki/api/v1/labels")))
    if v == "bad":
        vals = get(base, "/loki/api/v1/label/uri/values")
        print(f"  uri 라벨 값 {len(vals)}개, 예: {vals[0]}")
    now = int(time.time() * 1e9)
    res = get(base, "/loki/api/v1/query_range", query='{job="nginx"} |= "search"', limit=1,
              start=now - 3600 * 10**9, end=now)["result"]
    print("  저장된 줄 예:", res[0]["values"][0][1][:100] if res else "(없음)")
