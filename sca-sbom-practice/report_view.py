import html
import json
import sys

STYLE = """<style>
body{font:15px 'Malgun Gothic',sans-serif;margin:32px;color:#1f2933}
h1{font-size:22px;margin:0 0 6px}p{margin:0 0 18px;color:#52606d}
table{border-collapse:collapse;width:100%}
th,td{border:1px solid #d5dbe1;padding:8px 10px;text-align:left;vertical-align:top}
th{background:#f1f4f7;white-space:nowrap}.n{font-weight:700;color:#c62828}code{font-size:13px}
</style>"""


def audit_page(path):
    deps = json.load(open(path, encoding="utf-8"))["dependencies"]
    rows, total = [], 0
    for d in deps:
        vulns = {v["id"]: v for v in d["vulns"]}
        total += len(vulns)
        fixes = sorted({f for v in vulns.values() for f in v["fix_versions"]})
        ids = ", ".join(sorted(vulns))
        rows.append(
            f"<tr><td>{html.escape(d['name'])}</td><td>{d['version']}</td>"
            f"<td class='n'>{len(vulns)}</td><td>{html.escape(', '.join(fixes))}</td>"
            f"<td><code>{html.escape(ids)}</code></td></tr>"
        )
    head = "<tr><th>패키지</th><th>버전</th><th>취약점</th><th>수정 버전</th><th>ID</th></tr>"
    return (f"<!doctype html><meta charset='utf-8'><title>pip-audit 결과</title>{STYLE}"
            f"<h1>pip-audit 결과: 중복을 뺀 취약점 {total}건</h1><p>패키지 {len(deps)}개를 검사했습니다.</p>"
            f"<table>{head}{''.join(rows)}</table>")


def sbom_page(path):
    bom = json.load(open(path, encoding="utf-8"))
    rows = "".join(
        f"<tr><td>{html.escape(c['name'])}</td><td>{c['version']}</td><td><code>{html.escape(c['purl'])}</code></td></tr>"
        for c in bom["components"]
    )
    return (f"<!doctype html><meta charset='utf-8'><title>SBOM</title>{STYLE}"
            f"<h1>{bom['bomFormat']} {bom['specVersion']} SBOM: 구성요소 {len(bom['components'])}개</h1>"
            f"<p>serialNumber {bom['serialNumber']}</p>"
            f"<table><tr><th>이름</th><th>버전</th><th>purl</th></tr>{rows}</table>")


audit_json, sbom_json = sys.argv[1:3]
open("audit.html", "w", encoding="utf-8").write(audit_page(audit_json))
open("sbom.html", "w", encoding="utf-8").write(sbom_page(sbom_json))
