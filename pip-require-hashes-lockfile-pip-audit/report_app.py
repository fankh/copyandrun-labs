"""점검 결과를 브라우저로 보여 주는 작은 Flask 보고서.

사용법: python report_app.py [포트]
같은 폴더의 audit-old.json, audit-new.json(pip-audit -f json 결과)과
hash-ok.json, hash-tampered.json(hash_check.py 결과)을 읽어 두 화면을 만든다.
  /        pip-audit 점검 보고서 (고치기 전과 후)
  /hashes  해시 비교 (정상일 때와 내용이 바뀐 뒤)
"""
import html
import json
import sys
from pathlib import Path

from flask import Flask

BASE = Path(__file__).resolve().parent
app = Flask(__name__)

STYLE = """<style>
body{font:15px 'Malgun Gothic',sans-serif;margin:28px auto;max-width:1100px;color:#1f2933}
h1{font-size:22px;margin:0 0 6px}h2{font-size:17px;margin:26px 0 8px}p{margin:0 0 12px;color:#52606d}
table{border-collapse:collapse;width:100%;margin-bottom:6px}
th,td{border:1px solid #d5dbe1;padding:7px 10px;text-align:left;vertical-align:top}
th{background:#f1f4f7;white-space:nowrap}code{font-size:12.5px;word-break:break-all}
.bad{color:#b71c1c;font-weight:700}.ok{color:#1b7f3b;font-weight:700}
.cols{display:flex;gap:18px}.cols>div{flex:1;min-width:0}
.box{border:1px solid #d5dbe1;border-radius:6px;padding:12px 14px}
</style>"""


def load(name):
    return json.loads((BASE / name).read_text(encoding="utf-8"))


def audit_table(data):
    rows, total = [], 0
    for dep in data["dependencies"]:
        vulns = {v["id"]: v for v in dep.get("vulns", [])}
        total += len(vulns)
        fixes = sorted({f for v in vulns.values() for f in v["fix_versions"]})
        cls = "bad" if vulns else "ok"
        rows.append(
            f"<tr><td>{html.escape(dep['name'])}</td><td>{html.escape(str(dep.get('version', '')))}</td>"
            f"<td class='{cls}'>{len(vulns)}</td><td>{html.escape(', '.join(fixes)) or '-'}</td>"
            f"<td><code>{html.escape(', '.join(sorted(vulns))) or '-'}</code></td></tr>"
        )
    head = "<tr><th>패키지</th><th>버전</th><th>취약점</th><th>수정 버전</th><th>ID</th></tr>"
    return total, f"<table>{head}{''.join(rows)}</table>"


@app.get("/")
def audit_page():
    old_total, old_table = audit_table(load("audit-old.json"))
    new_total, new_table = audit_table(load("audit-new.json"))
    return (
        f"<!doctype html><meta charset='utf-8'><title>의존성 점검 보고서</title>{STYLE}"
        "<h1>의존성 점검 보고서</h1>"
        "<p>같은 requirements를 pip-audit로 점검한 결과입니다. 취약점은 중복을 뺀 건수입니다.</p>"
        f"<h2>고치기 전: requirements-old.txt <span class='bad'>취약점 {old_total}건</span></h2>{old_table}"
        f"<h2>고친 뒤: requirements.in <span class='ok'>취약점 {new_total}건</span></h2>{new_table}"
    )


def hash_box(title, data):
    rows = []
    for r in data["rows"]:
        verdict = "<span class='ok'>일치</span>" if r["match"] else "<span class='bad'>불일치</span>"
        rows.append(
            f"<tr><td>{html.escape(r['name'])} {html.escape(r['version'])}</td>"
            f"<td><code>{html.escape(r['file'])}</code></td></tr>"
            f"<tr><th>잠금 파일</th><td><code>{html.escape(', '.join(r['locked']))}</code></td></tr>"
            f"<tr><th>서버가 내준 파일</th><td><code>{r['actual']}</code></td></tr>"
            f"<tr><th>판정</th><td>{verdict}</td></tr>"
        )
    return f"<div class='box'><h2>{html.escape(title)}</h2><table>{''.join(rows)}</table></div>"


@app.get("/hashes")
def hashes_page():
    ok, bad = load("hash-ok.json"), load("hash-tampered.json")
    return (
        f"<!doctype html><meta charset='utf-8'><title>해시 불일치 전후 비교</title>{STYLE}"
        "<h1>해시 불일치 전후 비교</h1>"
        "<p>같은 이름과 같은 버전인데 서버가 내주는 파일의 내용이 바뀌면 sha256 값이 달라집니다.</p>"
        f"<div class='cols'>{hash_box('정상일 때', ok)}{hash_box('내용이 바뀐 뒤', bad)}</div>"
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(sys.argv[1]) if len(sys.argv) > 1 else 19810)
