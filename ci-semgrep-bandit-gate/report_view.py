import html
import json
import sys


def bandit_rows(path):
    for r in json.load(open(path, encoding="utf-8"))["results"]:
        where = f'{r["filename"]}:{r["line_number"]}'
        yield "Bandit", r["issue_severity"], r["test_id"], where, r["issue_text"]


def semgrep_rows(path):
    run = json.load(open(path, encoding="utf-8"))["runs"][0]
    levels = {r["id"]: r.get("defaultConfiguration", {}).get("level", "error") for r in run["tool"]["driver"]["rules"]}
    for r in run["results"]:
        loc = r["locations"][0]["physicalLocation"]
        where = f'{loc["artifactLocation"]["uri"]}:{loc["region"]["startLine"]}'
        yield "Semgrep", levels.get(r["ruleId"], "error").upper(), r["ruleId"].split(".")[-1], where, r["message"]["text"].splitlines()[0]


bandit_json, semgrep_sarif, out = sys.argv[1:4]
rows = list(bandit_rows(bandit_json)) + list(semgrep_rows(semgrep_sarif))
ok = not rows
body = "".join(
    f"<tr><td>{t}</td><td><b class='s {s.lower()}'>{s}</b></td><td>{html.escape(r)}</td>"
    f"<td><code>{html.escape(w)}</code></td><td>{html.escape(m)}</td></tr>"
    for t, s, r, w, m in rows
)
page = f"""<!doctype html><meta charset="utf-8"><title>SAST 게이트 결과</title>
<style>
body{{font:15px 'Malgun Gothic',sans-serif;margin:32px;color:#1f2933}}
.banner{{padding:14px 18px;border-radius:8px;font-weight:700;font-size:18px;color:#fff;background:{'#2e7d32' if ok else '#c62828'}}}
table{{border-collapse:collapse;width:100%;margin-top:20px}}
th,td{{border:1px solid #d5dbe1;padding:8px 10px;text-align:left;vertical-align:top}}
th{{background:#f1f4f7}}
.s{{padding:2px 8px;border-radius:4px;color:#fff;background:#c62828}}.s.warning,.s.medium{{background:#ef6c00}}
</style>
<div class="banner">{'게이트 통과: 발견 사항 0건' if ok else f'게이트 실패: 발견 사항 {len(rows)}건'}</div>
<table><tr><th>도구</th><th>심각도</th><th>룰</th><th>위치</th><th>설명</th></tr>{body}</table>"""
open(out, "w", encoding="utf-8").write(page)
