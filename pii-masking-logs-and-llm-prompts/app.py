"""회원가입, 결제, 챗 문의를 받는 Flask 앱입니다. MASK=1 이면 로그와 프롬프트에서 개인정보를 가립니다."""
import json
import logging
import os
import re
import sys
import urllib.request
from datetime import datetime, timezone

from flask import Flask, jsonify, request

from pii import PiiFilter, mask_text

MASK = os.environ.get("MASK", "0") == "1"
MODE = "after" if MASK else "before"
LLM_URL = os.environ.get("LLM_URL", "http://llm:8000/v1/chat")
LOG_PATH = f"/logs/app-{MODE}.log"
ANSI = re.compile(r"\x1b\[[0-9;]*m")  # werkzeug 가 붙이는 색상 코드
CUSTOMERS = {"010-1234-5678": "테스트고객1"}  # 전부 실습용 가짜 값입니다


class JsonFormatter(logging.Formatter):
    def format(self, record):
        doc = {
            "@timestamp": datetime.fromtimestamp(record.created, timezone.utc).isoformat(),
            "mode": MODE,
            "level": record.levelname,
            "logger": record.name,
            "message": ANSI.sub("", record.getMessage()),
        }
        if record.exc_info:
            doc["exception"] = record.exc_text or self.formatException(record.exc_info)
        return json.dumps(doc, ensure_ascii=False)


def setup_logging():
    handlers = [logging.FileHandler(LOG_PATH, mode="w", encoding="utf-8"), logging.StreamHandler(sys.stdout)]
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    for handler in handlers:
        handler.setFormatter(JsonFormatter())
        if MASK:
            handler.addFilter(PiiFilter())  # 로거가 아니라 핸들러에 붙여야 다른 로거(werkzeug 등)의 기록도 가려집니다
        root.addHandler(handler)


setup_logging()
log = logging.getLogger("shop")
app = Flask(__name__)


def ask_llm(prompt):
    body = json.dumps({"mode": MODE, "prompt": prompt}).encode()
    req = urllib.request.Request(LLM_URL, body, {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=10) as res:
        return json.load(res)["answer"]


@app.get("/health")
def health():
    return jsonify(ok=True)


@app.post("/signup")
def signup():
    d = request.get_json()
    log.info("회원가입 요청: name=%s rrn=%s phone=%s email=%s", d["name"], d["rrn"], d["phone"], d["email"])
    return jsonify(ok=True)


@app.post("/payment")
def payment():
    d = request.get_json()
    log.info("결제 요청: card=%s amount=%s memo=%s", d["card"], d["amount"], d.get("memo", ""))
    return jsonify(ok=True)


@app.post("/chat")
def chat():
    message = request.get_json()["message"]
    prompt = "다음 고객 문의를 두 문장으로 요약하세요.\n" + message
    if MASK:
        prompt = mask_text(prompt, style="prompt")  # LLM 호출 직전 전처리
    log.info("LLM 호출: prompt=%s", prompt.replace("\n", " / "))
    return jsonify(answer=ask_llm(prompt))


@app.get("/lookup")
def lookup():
    phone = request.args["phone"]
    name = CUSTOMERS.get(phone)
    if name is None:
        try:
            raise LookupError(f"고객을 찾지 못했습니다: {phone}")
        except LookupError:
            log.exception("고객 조회 실패")
        return jsonify(found=False), 404
    return jsonify(found=True, name=name)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
