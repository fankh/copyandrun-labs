import html
import json
import sys

STYLE = """<style>
body{font:15px 'Malgun Gothic',sans-serif;margin:32px;color:#1f2933}
h1{font-size:22px;margin:0 0 14px}
.sum{display:flex;gap:12px;margin-bottom:20px}
.box{padding:12px 20px;border-radius:8px;color:#fff;font-weight:700;font-size:18px}
.p{background:#2e7d32}.f{background:#c62828}.s{background:#546e7a}
table{border-collapse:collapse;width:100%}
th,td{border:1px solid #d5dbe1;padding:7px 10px;text-align:left;vertical-align:top}
th{background:#f1f4f7}code{font-size:13px}.tag{font-weight:700}
.FAILED{color:#c62828}.SKIPPED{color:#546e7a}
</style>"""


def rows(results, state):
    for c in results:
        note = c["check_result"].get("suppress_comment", "") if state == "SKIPPED" else ""
        yield (
            f"<tr><td class='tag {state}'>{state}</td><td><code>{c['check_id']}</code></td>"
            f"<td>{html.escape(c['check_name'])}</td><td><code>{html.escape(c['resource'])}</code></td>"
            f"<td>{c['file_line_range'][0]}-{c['file_line_range'][1]}</td><td>{html.escape(note)}</td></tr>"
        )


report_json, out, title = sys.argv[1:4]
d = json.load(open(report_json, encoding="utf-8"))
s, r = d["summary"], d["results"]
body = list(rows(r.get("failed_checks", []), "FAILED")) + list(rows(r.get("skipped_checks", []), "SKIPPED"))
page = (
    f"<!doctype html><meta charset='utf-8'><title>Checkov 결과</title>{STYLE}<h1>{html.escape(title)}</h1>"
    f"<div class='sum'><div class='box p'>통과 {s['passed']}</div><div class='box f'>실패 {s['failed']}</div>"
    f"<div class='box s'>예외 {s['skipped']}</div></div>"
    f"<table><tr><th>상태</th><th>검사 ID</th><th>검사 내용</th><th>리소스</th><th>줄</th><th>예외 사유</th></tr>{''.join(body)}</table>"
)
open(out, "w", encoding="utf-8").write(page)
