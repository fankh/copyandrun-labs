"""에이전트 두 개(mail-bot, ops-bot)가 번갈아 도구를 호출합니다. 모델 호출은 없습니다."""
import json
import sys
import time
import urllib.error
import urllib.request

PROXY = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:5742"

MAIL = ("mail-bot", "sess-m1")
OPS = ("ops-bot", "sess-o1")

# (에이전트, 실행 ID, 도구, 인자, 승인 번호)
STEPS = [
    (MAIL, "run-mail-01", "read_file", {"path": "report.txt"}, None),
    (OPS, "run-ops-01", "read_file", {"path": "old-backup.txt"}, None),
    (MAIL, "run-mail-01", "send_mail", {"to": "alice", "subject": "3분기 보고서", "body": "초안입니다. api_key=sk-test-12345"}, None),
    (OPS, "run-ops-01", "delete_file", {"path": "old-backup.txt"}, None),
    (MAIL, "run-mail-02", "delete_file", {"path": "notes.txt"}, "CHG-1042"),
    (OPS, "run-ops-01", "read_file", {"path": "missing.txt"}, None),
    (OPS, "run-ops-02", "read_file", {"path": "report.txt"}, None),
    (MAIL, "run-mail-02", "send_mail", {"to": "carol", "subject": "정리 완료", "body": "메모를 정리했습니다."}, None),
    (OPS, "run-ops-02", "delete_file", {"path": "report.txt"}, None),
]

for (agent, session), run, tool, args, approval in STEPS:
    headers = {"Content-Type": "application/json", "X-Agent-Id": agent, "X-Session-Id": session, "X-Run-Id": run}
    if approval:
        headers["X-Approval-Id"] = approval
    req = urllib.request.Request(f"{PROXY}/tools/{tool}", json.dumps({"args": args}).encode(), headers, method="POST")
    try:
        code = urllib.request.urlopen(req).status
    except urllib.error.HTTPError as exc:
        code = exc.code
    print(f"{agent:9} {run:11} {tool:12} HTTP {code}")
    time.sleep(0.4)
