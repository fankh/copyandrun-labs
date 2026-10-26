"""숨은 문자를 드러내 보여 주는 작은 웹 뷰어. samples 폴더(make_samples.py 가 만듦)를 읽습니다.

samples 폴더가 있는 곳에서 python viewer_app.py 로 띄우고 http://127.0.0.1:5431 을 엽니다.
"""
import html
from pathlib import Path

from flask import Flask, abort, request

from agent_config_scan import hidden_class, render_html, scan

app = Flask(__name__)
SAMPLES = Path("samples")   # 이 폴더에서 실행합니다
REPOS = {"bad": "오염된 저장소", "clean": "정상 저장소"}

STYLE = """<meta charset="utf-8"><style>
body{font-family:"Malgun Gothic",sans-serif;margin:0;background:#f4f5f7;color:#1f2933}
header{background:#1f2933;color:#fff;padding:14px 28px;font-size:18px}
main{padding:20px 28px;max-width:1100px}
a{color:#1d4ed8}
table{border-collapse:collapse;width:100%;background:#fff}
td,th{border:1px solid #d5d9de;padding:6px 10px;text-align:left;font-size:14px;vertical-align:top}
th{background:#e4e7eb}
.no{width:36px;color:#52606d}
.ed{width:42%;font-family:Consolas,"Malgun Gothic",monospace;unicode-bidi:isolate;white-space:pre-wrap}
.cp{font-family:Consolas,"Malgun Gothic",monospace;white-space:pre-wrap;word-break:break-all}
.chip{background:#b42318;color:#fff;border-radius:3px;padding:0 3px;margin:0 1px;font-size:12px}
.sum{background:#fff;border:1px solid #d5d9de;border-radius:8px;padding:10px 16px;margin:12px 0}
</style>"""


def page(title, body):
    return f"<!doctype html><html lang='ko'><title>{html.escape(title)}</title>{STYLE}<header>{html.escape(title)}</header><main>{body}</main></html>"


def files_of(repo):
    if repo not in REPOS:
        abort(404)
    base = SAMPLES / repo
    return base, sorted(p for p in base.rglob("*") if p.is_file())


@app.get("/")
def index():
    out = ""
    for repo, label in REPOS.items():
        base, files = files_of(repo)
        links = "".join(
            f"<li><a href='/view?repo={repo}&file={p.relative_to(base).as_posix()}'>{p.relative_to(base).as_posix()}</a></li>"
            for p in files)
        out += f"<h2>{label} ({repo})</h2><ul>{links}</ul><p><a href='/report?repo={repo}'>스캔 보고서 보기</a></p>"
    return page("규칙 파일 뷰어", out)


@app.get("/view")
def view():
    repo, rel = request.args.get("repo", ""), request.args.get("file", "")
    base, files = files_of(repo)
    path = next((p for p in files if p.relative_to(base).as_posix() == rel), None)
    if path is None:
        abort(404)
    text = path.read_text(encoding="utf-8")
    rows, hidden_total = "", 0
    for n, line in enumerate(text.split("\n"), 1):
        if not line:
            continue
        chips = "".join(
            f"<span class='chip'>U+{ord(c):04X}</span>" if hidden_class(c) else html.escape(c) for c in line)
        hidden_total += sum(bool(hidden_class(c)) for c in line)
        rows += f"<tr><td class='no'>{n}</td><td class='ed'>{html.escape(line)}</td><td class='cp'>{chips}</td></tr>"
    visible = sum(1 for c in text if not hidden_class(c))
    summary = (f"<div class='sum'>글자 {len(text)}개, 바이트 {len(text.encode('utf-8'))}개. "
               f"눈에 보이는 쪽으로 센 글자 {visible}개, 숨은 문자 <b>{hidden_total}</b>개.</div>")
    body = (f"<p><a href='/'>목록</a> / {REPOS[repo]} / <b>{html.escape(rel)}</b></p>{summary}"
            "<table><tr><th>줄</th><th>에디터에서 보이는 모습</th><th>코드포인트로 본 모습</th></tr>" + rows + "</table>")
    return page("규칙 파일 뷰어", body)


@app.get("/report")
def report():
    repo = request.args.get("repo", "")
    files_of(repo)
    files, findings = scan([SAMPLES / repo])
    return render_html(files, findings)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5431)
