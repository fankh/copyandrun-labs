"""OWASP Agentic Top 10 항목별 대응 현황 표를 브라우저로 보여 주는 작은 Flask 앱.

실행: pip install flask && python asi_table.py
열기: http://127.0.0.1:5410/?filter=all  (tested, partial, untested 도 가능)
"""
import json
from html import escape
from pathlib import Path

from flask import Flask, request

BASE = Path(__file__).resolve().parent
DATA = json.loads((BASE / "asi_mapping.json").read_text(encoding="utf-8"))
SITE = "https://copyandrun.com/blog/"
LABELS = DATA["status_labels"]
FILTERS = [("all", "전체"), ("tested", "시험함"), ("partial", "일부만"), ("untested", "미시험")]

app = Flask(__name__)

CSS = """
body{font-family:'Malgun Gothic',sans-serif;margin:24px;background:#f6f7f9;color:#1d2330}
h1{font-size:20px;margin:0 0 4px}
.sub{color:#5b6475;font-size:13px;margin-bottom:14px}
.tabs a{display:inline-block;padding:6px 14px;margin-right:6px;border:1px solid #c9ced8;border-radius:6px;
 text-decoration:none;color:#1d2330;background:#fff;font-size:14px}
.tabs a.on{background:#1f4fd8;color:#fff;border-color:#1f4fd8}
table{border-collapse:collapse;width:100%;background:#fff;margin-top:14px;font-size:14px}
th,td{border:1px solid #d5d9e2;padding:8px 10px;text-align:left;vertical-align:top}
th{background:#eceff5}
.tag{display:inline-block;padding:2px 8px;border-radius:10px;font-size:12px;font-weight:700;white-space:nowrap}
.tested{background:#d8f0dc;color:#17602a}.partial{background:#fff0c9;color:#7a5200}.untested{background:#e6e8ee;color:#444b5a}
.fact{margin:0 0 6px}.scope{color:#5b6475;font-size:13px}
a{color:#1f4fd8}
"""


def row(item):
    status = item["status"]
    posts = "".join(
        f'<p class="fact"><a href="{SITE}{p["slug"]}/">{escape(p["slug"])}</a><br>{escape(p["fact"])}</p>'
        for p in item["posts"]
    ) or '<p class="fact">이 항목을 다룬 글이 아직 없습니다.</p>'
    checks = "".join(f"<li>{escape(c)}</li>" for c in item["checklist"])
    check_html = f"<ul>{checks}</ul>" if checks else "-"
    return (
        f'<tr><td><b>{item["id"]}</b><br>{escape(item["title_en"])}</td>'
        f'<td>{escape(item["summary"])}</td>'
        f'<td><span class="tag {status}">{LABELS[status]}</span><div class="scope">{escape(item["scope"])}</div></td>'
        f"<td>{posts}</td><td>{check_html}</td></tr>"
    )


@app.route("/")
def index():
    flt = request.args.get("filter", "all")
    items = [i for i in DATA["items"] if flt == "all" or i["status"] == flt]
    tabs = "".join(
        f'<a class="{"on" if k == flt else ""}" href="/?filter={k}">{name}</a>' for k, name in FILTERS
    )
    count = {k: sum(1 for i in DATA["items"] if i["status"] == k) for k in LABELS}
    head = f"시험함 {count['tested']} / 일부만 {count['partial']} / 미시험 {count['untested']}"
    return (
        f"<!doctype html><meta charset='utf-8'><title>ASI 대응 현황</title><style>{CSS}</style>"
        f"<h1>OWASP Agentic Top 10 항목별 대응 현황</h1><div class='sub'>{head} (총 10개)</div>"
        f"<div class='tabs'>{tabs}</div>"
        "<table><tr><th>항목</th><th>한 줄 설명</th><th>시험 상태</th><th>확인한 글과 관찰</th><th>점검 체크리스트</th></tr>"
        + "".join(row(i) for i in items)
        + "</table>"
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5410)
