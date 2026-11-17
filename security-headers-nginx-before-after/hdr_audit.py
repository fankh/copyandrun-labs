#!/usr/bin/env python3
"""저장해 둔 응답 헤더(.hdr 파일)를 검사해 경로별 결과를 보여 주고, 하나라도 기준을 어기면 종료 코드 1로 끝낸다.
사용: python hdr_audit.py 폴더 설정이름   (파일 이름 형식: 설정이름__경로이름.hdr)"""
import glob
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")

REQUIRED = [
    "strict-transport-security",
    "content-security-policy",
    "x-content-type-options",
    "referrer-policy",
    "permissions-policy",
]
folder, name = sys.argv[1], sys.argv[2]
failed = False
print(f"== {name}")
for path in sorted(glob.glob(os.path.join(folder, f"{name}__*.hdr"))):
    label = os.path.basename(path)[len(name) + 2:-4]
    lines = [l.rstrip("\r\n") for l in open(path, encoding="utf-8") if l.strip()]
    status = lines[0].split()[1]
    headers = {}
    cookies = []
    for line in lines[1:]:
        k, _, v = line.partition(":")
        k, v = k.strip().lower(), v.strip()
        headers[k] = v
        if k == "set-cookie":
            cookies.append(v)
    have = sum(1 for h in REQUIRED if h in headers)
    notes = []
    server = headers.get("server", "")
    if "/" in server:
        notes.append(f"Server 버전 노출({server})")
    for c in cookies:
        low = c.lower()
        miss = [f for f in ("httponly", "secure", "samesite") if f not in low]
        if miss:
            notes.append("쿠키에 " + "·".join(miss) + " 없음")
    ok = have == len(REQUIRED) and not notes
    failed |= not ok
    print(f"  {label:<8} HTTP {status}  보안 헤더 {have}/{len(REQUIRED)}  {'통과' if ok else '실패'}  {'; '.join(notes)}")
sys.exit(1 if failed else 0)
