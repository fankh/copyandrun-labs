import os
from html import escape
from string import Template

from flask import Flask, request

from agent import secure_read, secure_write, vuln_read, vuln_write

app = Flask(__name__)

PAGE = Template("""<!doctype html>
<html lang="ko"><meta charset="utf-8">
<title>도구 권한 비교</title>
<style>
body{font-family:"Malgun Gothic",sans-serif;margin:0;background:#f4f5f7;color:#1f2933}
header{background:#1f2933;color:#fff;padding:14px 28px;font-size:18px}
main{padding:20px 28px;max-width:1100px}
form{background:#fff;border:1px solid #d5d9de;border-radius:8px;padding:14px 18px;display:flex;gap:12px;flex-wrap:wrap;align-items:end}
label{display:flex;flex-direction:column;font-size:13px;gap:4px}
input,select{font:inherit;padding:6px 8px;border:1px solid #aab2bb;border-radius:4px}
input[name=path]{width:360px}
button{font:inherit;padding:7px 18px;background:#2a6fdb;color:#fff;border:0;border-radius:4px}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:16px}
.box{background:#fff;border:1px solid #d5d9de;border-radius:8px;padding:12px 16px}
.box h2{margin:0 0 8px;font-size:16px}
.vuln h2{color:#b42318}.sec h2{color:#067647}
pre{margin:0;white-space:pre-wrap;word-break:break-all;background:#101418;color:#e6e6e6;padding:10px;border-radius:4px;min-height:24px}
.block pre{color:#ffb4a8}
.files{margin-top:16px}
</style>
<header>에이전트 파일 도구 비교 (취약 도구와 보안 도구)</header>
<main>
<form method="get">
<label>동작<select name="op"><option value="read"${r}>읽기</option><option value="write"${w}>쓰기</option></select></label>
<label>경로<input name="path" value="${path}"></label>
<label>쓸 내용<input name="content" value="${content}"></label>
<button>도구 호출</button>
</form>
${result}
<div class="box files"><h2>workspace 폴더 현황</h2><pre>${tree}</pre></div>
</main></html>""")


def tree():
    lines = []
    for base in ("allowed", "forbidden", "output"):
        d = os.path.join("workspace", base)
        names = sorted(os.listdir(d)) if os.path.isdir(d) else []
        lines.append(f"workspace/{base}/  " + (", ".join(names) if names else "(비어 있음)"))
    return "\n".join(lines)


@app.get("/")
def index():
    op = request.args.get("op", "read")
    path = request.args.get("path", "workspace/allowed/readme.txt")
    content = request.args.get("content", "정상 출력")
    result = ""
    if "path" in request.args:
        if op == "read":
            v, s = vuln_read(path), secure_read(path)
        else:
            v, s = vuln_write(path, content), secure_write(path, content)
        cls = " block" if s.startswith("[차단]") else ""
        result = (
            '<div class="cols">'
            f'<div class="box vuln"><h2>취약 도구</h2><pre>{escape(v)}</pre></div>'
            f'<div class="box sec{cls}"><h2>보안 도구</h2><pre>{escape(s)}</pre></div>'
            "</div>"
        )
    return PAGE.substitute(
        r=" selected" if op == "read" else "",
        w=" selected" if op == "write" else "",
        path=escape(path, quote=True),
        content=escape(content, quote=True),
        result=result,
        tree=escape(tree()),
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5400)
