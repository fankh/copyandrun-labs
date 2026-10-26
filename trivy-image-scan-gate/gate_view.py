import html
import json
import sys

STYLE = """<style>
body{font:15px 'Malgun Gothic',sans-serif;margin:32px;color:#1f2933}
h1{font-size:22px;margin:0 0 18px}
.cards{display:flex;gap:16px}
.card{flex:1;border:1px solid #d5dbe1;border-radius:8px;padding:16px}
.card h2{font-size:16px;margin:0 0 10px}
.verdict{display:inline-block;padding:3px 12px;border-radius:5px;color:#fff;font-weight:700;margin-bottom:12px}
.fail{background:#c62828}.pass{background:#2e7d32}
.row{display:flex;align-items:center;gap:8px;margin:6px 0}
.row span{width:90px}.bar{height:16px;border-radius:3px}
.c{background:#b71c1c}.h{background:#ef6c00}
.pkg{font-size:13px;color:#52606d;margin-top:10px}
</style>"""


def count(path):
    totals = {"CRITICAL": 0, "HIGH": 0}
    detail = []
    for r in json.load(open(path, encoding="utf-8")).get("Results", []):
        vulns = r.get("Vulnerabilities") or []
        for v in vulns:
            totals[v["Severity"]] += 1
        detail.append(f"{r['Target']}: {len(vulns)}건")
    return totals, detail


cards = ""
for arg in sys.argv[2:]:
    label, path, code = arg.split(":")
    totals, detail = count(path)
    verdict = "<div class='verdict pass'>통과 exit=0</div>" if code == "0" else f"<div class='verdict fail'>실패 exit={code}</div>"
    bars = "".join(
        f"<div class='row'><span>{name}</span><div class='bar {cls}' style='width:{max(totals[name] * 3, 2)}px'></div><b>{totals[name]}</b></div>"
        for name, cls in (("CRITICAL", "c"), ("HIGH", "h"))
    )
    cards += f"<div class='card'><h2>{html.escape(label)}</h2>{verdict}{bars}<div class='pkg'>{'<br>'.join(map(html.escape, detail))}</div></div>"
page = f"<!doctype html><meta charset='utf-8'><title>빌드 게이트 비교</title>{STYLE}<h1>HIGH, CRITICAL 게이트 결과 비교</h1><div class='cards'>{cards}</div>"
open(sys.argv[1], "w", encoding="utf-8").write(page)
