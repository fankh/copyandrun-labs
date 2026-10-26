import sys
from html import escape

from check_quality import analyze

r = analyze(sys.argv[1])
out = sys.argv[2] if len(sys.argv) > 2 else "report.html"

missing_total = sum(len(h["missing"]) for h in r["hosts"].values())
cards = [
    ("전체 줄", r["total"], ""),
    ("파싱 실패", len(r["parse_failed"]), "bad"),
    ("중복", len(r["duplicates"]), "bad"),
    ("유실", missing_total, "bad"),
    ("시간 이상", len(r["delay_problems"]), "bad"),
    ("순서 역전", len(r["reversals"]), "bad"),
]
card_html = "".join(
    f'<div class="card {"bad" if cls and n else ""}"><b>{n}</b><span>{escape(name)}</span></div>'
    for name, n, cls in cards
)
host_rows = "".join(
    f"<tr><td>{escape(h)}</td><td>{v['count']}</td><td>{v['first']}~{v['last']}</td>"
    f"<td class=\"{'bad' if v['missing'] else 'ok'}\">{escape(str(v['missing']) if v['missing'] else '없음')}</td></tr>"
    for h, v in r["hosts"].items()
)
line_rows = ""
for n, line in enumerate(r["lines"], 1):
    why = r["bad_lines"].get(n, "")
    cls = ' class="flag"' if why else ""
    line_rows += f"<tr{cls}><td>{n}</td><td><code>{escape(line)}</code></td><td>{escape(why)}</td></tr>"

html = f"""<!doctype html>
<html lang="ko"><meta charset="utf-8">
<title>로그 품질 점검 보고서</title>
<style>
body{{font-family:"Malgun Gothic",sans-serif;margin:0;background:#f4f5f7;color:#1f2933}}
header{{background:#1f2933;color:#fff;padding:14px 28px;font-size:18px}}
main{{padding:20px 28px;max-width:1080px}}
.cards{{display:flex;gap:12px;flex-wrap:wrap}}
.card{{background:#fff;border:1px solid #d5d9de;border-radius:8px;padding:12px 20px;min-width:120px;display:flex;flex-direction:column}}
.card b{{font-size:28px}}.card span{{font-size:13px;color:#52606d}}
.card.bad{{border-color:#b42318;background:#fde7e4}}.card.bad b{{color:#b42318}}
h2{{font-size:16px;margin:22px 0 8px}}
table{{border-collapse:collapse;background:#fff;width:100%;font-size:14px}}
td,th{{border:1px solid #d5d9de;padding:5px 10px;text-align:left}}
th{{background:#e4e7eb}}
tr.flag{{background:#fde7e4}}
td.bad{{color:#b42318;font-weight:700}}td.ok{{color:#067647}}
code{{font-family:Consolas,monospace;font-size:13px}}
</style>
<header>로그 품질 점검 보고서 ({escape(sys.argv[1])})</header>
<main>
<div class="cards">{card_html}</div>
<h2>호스트별 일련번호</h2>
<table><tr><th>호스트</th><th>받은 건수</th><th>번호 범위</th><th>유실된 번호</th></tr>{host_rows}</table>
<h2>줄별 판정</h2>
<table><tr><th>줄</th><th>내용</th><th>문제</th></tr>{line_rows}</table>
</main></html>"""
open(out, "w", encoding="utf-8").write(html)
print("saved", out)
