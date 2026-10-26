"""에이전트 도구 호출 프록시: 도구를 실행하고, 호출마다 감사 기록을 OpenSearch 에 색인합니다."""
import json
import os
import re
import threading
import time
import urllib.request
from datetime import datetime, timezone

from flask import Flask, jsonify, request

OS_URL = os.environ.get("OS_URL", "http://opensearch:9200")
AUDIT = os.environ.get("AUDIT", "1") == "1"
INDEX = "agent-audit"
SANDBOX = "/data"
SERVICE_ACCOUNT = "svc-agent"  # 모든 에이전트가 함께 쓰는 서비스 계정

app = Flask(__name__)
seq_lock = threading.Lock()
seq_by_run = {}


def seed_sandbox():
    os.makedirs(SANDBOX, exist_ok=True)
    files = {
        "report.txt": "2026년 3분기 보안 점검 보고서 초안입니다.\n",
        "notes.txt": "회의 메모: 계정 정리 일정은 다음 주에 정합니다.\n",
        "old-backup.txt": "오래된 백업 목록입니다.\n",
    }
    for name, text in files.items():
        with open(os.path.join(SANDBOX, name), "w", encoding="utf-8") as f:
            f.write(text)


def safe_path(name):
    path = os.path.realpath(os.path.join(SANDBOX, name))
    if not path.startswith(SANDBOX + os.sep):
        raise ValueError("허용 폴더 밖의 경로입니다")
    return path


def read_file(args):
    with open(safe_path(args["path"]), encoding="utf-8") as f:
        text = f.read()
    return {"chars": len(text)}


def send_mail(args):
    return {"queued": True}  # 실제로 보내지 않고 보낸 것처럼만 답합니다


def delete_file(args):
    os.remove(safe_path(args["path"]))
    return {"deleted": args["path"]}


TOOLS = {
    "read_file": (read_file, "low"),
    "send_mail": (send_mail, "medium"),
    "delete_file": (delete_file, "high"),
}

SENSITIVE_KEY = re.compile(r"pass|token|secret|key|authorization", re.I)
SECRET_VALUE = re.compile(r"(?i)(token|password|passwd|secret|api[_-]?key)\s*[=:]\s*\S+")


def mask(value):
    text = str(value)
    text = SECRET_VALUE.sub(r"\1=***", text)
    return text if len(text) <= 60 else text[:60] + "..."


def summarize(args):
    parts = []
    for key in sorted(args):
        shown = "***" if SENSITIVE_KEY.search(key) else mask(args[key])
        parts.append(f"{key}={shown}")
    return ", ".join(parts)


def index_audit(doc):
    req = urllib.request.Request(
        f"{OS_URL}/{INDEX}/_doc?refresh=true",
        data=json.dumps(doc, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        urllib.request.urlopen(req, timeout=3).read()
    except Exception as exc:  # 색인에 실패해도 도구 호출은 막지 않고 오류만 남깁니다
        print(f"[audit] index failed: {exc}", flush=True)


@app.post("/tools/<tool>")
def call_tool(tool):
    started = time.perf_counter()
    agent_id = request.headers.get("X-Agent-Id", "unknown")
    session_id = request.headers.get("X-Session-Id", "unknown")
    run_id = request.headers.get("X-Run-Id", "unknown")
    approval = request.headers.get("X-Approval-Id", "none")
    args = (request.get_json(silent=True) or {}).get("args", {})

    status, code = "ok", 200
    if tool not in TOOLS:
        result, status, code = {"error": "unknown tool"}, "error", 404
    else:
        try:
            result = TOOLS[tool][0](args)
        except Exception as exc:
            result, status, code = {"error": str(exc)}, "error", 400
    duration_ms = round((time.perf_counter() - started) * 1000, 2)

    # 도구 서버가 원래 남기는 기록: 서비스 계정만 보입니다
    print(f"[tool-server] account={SERVICE_ACCOUNT} tool={tool} status={status}", flush=True)

    if AUDIT:
        with seq_lock:
            seq_by_run[run_id] = seq_by_run.get(run_id, 0) + 1
            seq = seq_by_run[run_id]
        index_audit({
            "@timestamp": datetime.now(timezone.utc).isoformat(timespec="milliseconds"),
            "service_account": SERVICE_ACCOUNT,
            "agent_id": agent_id,
            "session_id": session_id,
            "run_id": run_id,
            "seq": seq,
            "tool": tool,
            "risk": TOOLS[tool][1] if tool in TOOLS else "unknown",
            "args_summary": summarize(args),
            "approval": approval,
            "status": status,
            "duration_ms": duration_ms,
        })
    return jsonify(result), code


if __name__ == "__main__":
    seed_sandbox()
    app.run(host="0.0.0.0", port=8000)
