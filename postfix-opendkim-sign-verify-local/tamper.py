"""받은 메일(표준 입력)의 본문 1바이트를 바꿔 받는 서버에 다시 보냅니다. 사용법: tamper.py 보낸이 받는이"""
import re
import smtplib
import sys

raw = sys.stdin.buffer.read()
head, body = raw.split(b"\n\n", 1)
head = head.split(b"\n", 1)[1]                                        # mbox 첫 줄(From ...) 제거
head = re.sub(rb"(?m)^(?:Authentication-Results|Delivered-To|Return-Path):.*\n(?:[ \t].*\n)*", b"", head + b"\n").rstrip(b"\n")
body = body.replace(b"total 100", b"total 900", 1)                    # 1 -> 9, 딱 1바이트
with smtplib.SMTP("10.89.118.12", 25) as s:
    s.sendmail(sys.argv[1], [sys.argv[2]], head + b"\n\n" + body)
print("본문 1바이트를 바꿔 다시 보냈습니다.")
