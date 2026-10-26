from html import escape
from string import Template

import requests
from flask import Flask, request

import guard

app = Flask(__name__)

PAGE = Template("""<!doctype html>
<html lang="ko"><meta charset="utf-8">
<title>입력 가드레일 화면</title>
<style>
body{font-family:"Malgun Gothic",sans-serif;margin:0;background:#f4f5f7;color:#1f2933}
header{background:#1f2933;color:#fff;padding:14px 28px;font-size:18px}
main{padding:20px 28px;max-width:1000px}
form{background:#fff;border:1px solid #d5d9de;border-radius:8px;padding:14px 18px;display:flex;gap:12px;align-items:end}
input[name=text]{flex:1;font:inherit;padding:7px 9px;border:1px solid #aab2bb;border-radius:4px}
button{font:inherit;padding:7px 18px;background:#2a6fdb;color:#fff;border:0;border-radius:4px}
.box{background:#fff;border:1px solid #d5d9de;border-radius:8px;padding:12px 16px;margin-top:14px}
.box h2{margin:0 0 8px;font-size:16px}
table{border-collapse:collapse;width:100%}
td,th{border:1px solid #d5d9de;padding:6px 10px;text-align:left;font-size:14px}
th{background:#e4e7eb}
.pass{color:#067647;font-weight:700}.block{color:#b42318;font-weight:700}
.verdict{font-size:18px;padding:12px 16px;border-radius:8px;margin-top:14px}
.verdict.ok{background:#e3f6ec;border:1px solid #067647}
.verdict.no{background:#fde7e4;border:1px solid #b42318}
pre{margin:0;white-space:pre-wrap;word-break:break-all;background:#101418;color:#e6e6e6;padding:10px;border-radius:4px}
.hint{font-size:13px;color:#52606d;margin-top:8px}
</style>
<header>입력 가드레일 (규칙 필터, llama-guard3:1b, 판정 모델)</header>
<main>
<form method="get"><input name="text" value="${text}" placeholder="검사할 입력"><button>검사</button></form>
${result}
<div class="box"><h2>blocked.jsonl 마지막 3줄</h2><pre>${log}</pre></div>
</main></html>""")


def run_gate(fn, text):
    try:
        reason = fn(text)
    except (requests.RequestException, ValueError, KeyError) as e:
        return "오류", type(e).__name__
    return ("차단", reason) if reason else ("통과", "")


def log_tail():
    try:
        with open(guard.LOG_FILE, encoding="utf-8") as f:
            return "".join(f.readlines()[-3:]) or "(비어 있음)"
    except OSError:
        return "(아직 기록 없음)"


@app.get("/")
def index():
    text = request.args.get("text", "")
    result = ""
    if text:
        rows = ""
        for name, fn in (("규칙 필터", guard.rule_filter), ("llama-guard3:1b", guard.guard_model),
                         ("판정 모델 qwen2.5:1.5b", guard.judge_model)):
            state, reason = run_gate(fn, text)
            cls = "pass" if state == "통과" else "block"
            rows += f'<tr><td>{name}</td><td class="{cls}">{state}</td><td>{escape(str(reason))}</td></tr>'
        final = guard.handle(text)
        ok = final.startswith("PASS")
        result = (f'<div class="box"><h2>관문별 판정</h2><table><tr><th>관문</th><th>판정</th><th>사유</th></tr>{rows}</table>'
                  '<div class="hint">세 관문을 모두 따로 실행한 결과입니다. 실제 서비스는 앞 관문에서 걸리면 뒤 관문을 실행하지 않습니다.</div></div>'
                  f'<div class="verdict {"ok" if ok else "no"}">{escape(final)}</div>')
    return PAGE.substitute(text=escape(text, quote=True), result=result, log=escape(log_tail()))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5402)
