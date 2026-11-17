"""사서함의 각 메일에서 본문 해시를 직접 계산해 서명 안의 bh 값과 비교합니다. 사용법: bodyhash.py 사서함"""
import base64
import hashlib
import mailbox
import re
import sys

for i, msg in enumerate(mailbox.mbox(sys.argv[1])):
    raw = msg.as_bytes().split(b"\n\n", 1)[1]
    lines = [re.sub(rb"[ \t]+", b" ", ln).rstrip(b" \t") for ln in raw.split(b"\n")]      # relaxed 본문 정규화
    body = b"\r\n".join(lines).rstrip(b"\r\n") + b"\r\n"
    mine = base64.b64encode(hashlib.sha256(body).digest()).decode()
    sig = re.sub(r"\s+", "", msg["DKIM-Signature"])
    signed = re.search(r"bh=([^;]+);", sig).group(1)
    print(f"메일 {i}: 계산한 해시 {mine[:12]}... 서명의 bh {signed[:12]}... {'일치' if mine == signed else '불일치'}")
