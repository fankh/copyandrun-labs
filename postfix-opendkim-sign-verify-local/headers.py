"""사서함에서 n번째 메일의 DKIM 관련 헤더만 골라 보여 줍니다. 사용법: headers.py 사서함 번호"""
import mailbox
import sys

msg = list(mailbox.mbox(sys.argv[1]))[int(sys.argv[2])]
for name in ("DKIM-Signature", "Authentication-Results", "Subject"):
    for value in msg.get_all(name, []):
        print(f"{name}: {value}")
