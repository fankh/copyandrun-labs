import json
import sys
from html import escape
from pathlib import Path

from flask import Flask, abort

app = Flask(__name__)
REPORTS = {}  # 이름 -> 발견 항목 목록

CSS = """
body{font:15px 'Malgun Gothic',sans-serif;margin:0;color:#1f2933;background:#f6f8fa}
header{background:#24292f;color:#fff;padding:14px 32px}
header a{color:#9ecbff;margin-right:18px;text-decoration:none}
main{padding:24px 32px}
.banner{padding:14px 18px;border-radius:8px;font-weight:700;font-size:18px;color:#fff}
.fail{background:#c62828}.pass{background:#2e7d32}
table{border-collapse:collapse;width:100%;margin-top:20px;background:#fff}
th,td{border:1px solid #d5dbe1;padding:8px 10px;text-align:left;vertical-align:top}
th{background:#f1f4f7}
.sev{padding:2px 8px;border-radius:4px;color:#fff;font-weight:700;font-size:13px}
.high{background:#c62828}.medium{background:#ef6c00}.low{background:#6b7280}.informational{background:#6b7280}
pre{background:#0d1117;color:#e6edf3;padding:14px;border-radius:6px;overflow:auto;font-size:14px;line-height:1.5}
.note{background:#fff8e1;border-left:4px solid #f9a825;padding:10px 14px;margin:14px 0}
dl{display:grid;grid-template-columns:120px 1fr;gap:6px 12px;background:#fff;padding:14px;border:1px solid #d5dbe1}
dt{font-weight:700}dd{margin:0}
"""


def load(path):
    out = []
    for f in json.loads(Path(path).read_text(encoding="utf-8")):
        loc = f["locations"][0]
        out.append({
            "rule": f["ident"],
            "desc": f["desc"],
            "url": f["url"],
            "severity": f["determinations"]["severity"],
            "confidence": f["determinations"]["confidence"],
            "persona": f["determinations"]["persona"],
            "file": loc["symbolic"]["key"]["Local"]["verbatim_path"].replace("\\", "/"),
            "line": loc["concrete"]["location"]["start_point"]["row"] + 1,
            "note": loc["symbolic"].get("annotation", ""),
            "snippet": loc["concrete"]["feature"],
            "fixes": [x["title"] for x in f.get("fixes", [])],
        })
    out.sort(key=lambda x: (x["file"], x["line"]))
    return out


def page(title, body):
    nav = "".join(f'<a href="/r/{n}">{escape(n)}</a>' for n in REPORTS)
    return (f'<!doctype html><meta charset="utf-8"><title>{escape(title)}</title><style>{CSS}</style>'
            f'<header><b>zizmor 보고서 뷰어</b> &nbsp; {nav}</header><main>{body}</main>')


@app.route("/")
def index():
    rows = "".join(
        f'<tr><td><a href="/r/{n}">{escape(n)}</a></td><td>{len(items)}</td></tr>'
        for n, items in REPORTS.items()
    )
    return page("보고서 목록", f"<h2>보고서 목록</h2><table><tr><th>이름</th><th>발견 항목</th></tr>{rows}</table>")


@app.route("/r/<name>")
def report(name):
    items = REPORTS.get(name)
    if items is None:
        abort(404)
    ok = not items
    banner = "발견 항목 0건: 점검 통과" if ok else f"발견 항목 {len(items)}건: 수정 필요"
    rows = "".join(
        f'<tr><td><span class="sev {x["severity"].lower()}">{x["severity"]}</span></td>'
        f'<td><a href="/r/{name}/{i}">{escape(x["rule"])}</a></td>'
        f'<td><code>{escape(x["file"])}:{x["line"]}</code></td><td>{escape(x["desc"])}</td></tr>'
        for i, x in enumerate(items)
    )
    table = "" if ok else f"<table><tr><th>심각도</th><th>규칙</th><th>위치</th><th>설명</th></tr>{rows}</table>"
    body = f'<div class="banner {"pass" if ok else "fail"}">{banner}</div>{table}'
    return page(f"{name} 보고서", body)


@app.route("/r/<name>/<int:i>")
def detail(name, i):
    items = REPORTS.get(name)
    if items is None or i >= len(items):
        abort(404)
    x = items[i]
    fixes = ", ".join(x["fixes"]) or "자동 수정 없음"
    body = (
        f'<h2>{escape(x["rule"])}</h2>'
        f'<dl><dt>설명</dt><dd>{escape(x["desc"])}</dd>'
        f'<dt>심각도</dt><dd><span class="sev {x["severity"].lower()}">{x["severity"]}</span> (확신도 {x["confidence"]})</dd>'
        f'<dt>위치</dt><dd><code>{escape(x["file"])}:{x["line"]}</code></dd>'
        f'<dt>자동 수정</dt><dd>{escape(fixes)}</dd>'
        f'<dt>문서</dt><dd>{escape(x["url"])}</dd></dl>'
        f'<div class="note">{escape(x["note"])}</div>'
        f'<pre>{escape(x["snippet"])}</pre>'
        f'<p><a href="/r/{name}">목록으로</a></p>'
    )
    return page(x["rule"], body)


if __name__ == "__main__":
    # 사용법: python viewer.py 이름=보고서.json [이름=보고서.json ...] [--port 5311]
    args = sys.argv[1:]
    port = 5311
    if "--port" in args:
        k = args.index("--port")
        port = int(args[k + 1])
        del args[k:k + 2]
    for a in args:
        n, p = a.split("=", 1)
        REPORTS[n] = load(p)
    app.run(host="127.0.0.1", port=port)
