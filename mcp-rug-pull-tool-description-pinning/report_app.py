"""pin_check.py 가 남긴 보고서(reports/*.json)를 브라우저로 보여 주는 작은 Flask 앱입니다."""
import json
from pathlib import Path

from flask import Flask, abort, render_template_string

app = Flask(__name__)
REPORTS = Path(__file__).parent / "reports"

PAGE = """<!doctype html><html lang="ko"><meta charset="utf-8"><title>MCP 도구 고정 점검</title>
<style>
body{font-family:"Malgun Gothic",sans-serif;margin:0;background:#f4f6f8;color:#1c2733}
header{background:#1c2733;color:#fff;padding:14px 28px}header h1{margin:0;font-size:20px}
main{padding:20px 28px;max-width:1100px}
.badge{display:inline-block;padding:4px 12px;border-radius:12px;font-weight:700;color:#fff}
.ok{background:#1a7f37}.bad{background:#c62828}.warn{background:#b26a00}
section{background:#fff;border:1px solid #d5dce3;border-radius:6px;padding:16px 20px;margin:16px 0}
h2{font-size:16px;margin:0 0 10px}
table{border-collapse:collapse;width:100%;font-size:14px}
th,td{border-bottom:1px solid #e3e8ed;padding:7px 10px;text-align:left}
th{background:#eef2f5}code{font-family:Consolas,monospace;font-size:13px}
.same{color:#1a7f37;font-weight:700}.diff{color:#c62828;font-weight:700}
pre{background:#0f1720;color:#d6dde4;padding:12px;border-radius:4px;font-size:13px;line-height:1.5;overflow:auto;margin:6px 0 0}
.add{color:#7ee787}.del{color:#ff7b72}.hdr{color:#8b98a5}
.meta{color:#5b6b7a;font-size:13px}
</style>
<header><h1>MCP 도구 고정 점검 보고서</h1></header>
<main>
<p><span class="badge {{ 'ok' if r.result == '일치' and not r.findings else ('bad' if r.result == '불일치' else 'warn') }}">
 해시 {{ r.result }}</span>
 <span class="meta">서버 {{ r.server }} / 점검 시각 {{ r.checked_at }}</span></p>

<section id="hashes"><h2>도구별 해시 비교</h2>
<table><tr><th>도구</th><th>이름</th><th>설명</th><th>입력 스키마</th><th>전체 해시 (고정 -&gt; 현재)</th></tr>
{% for t in r.tools %}<tr><td><b>{{ t.name }}</b></td>
{% for f in t.fields %}<td class="{{ 'same' if f.same else 'diff' }}">{{ '일치' if f.same else '변경' }}
 <br><code>{{ f.sha_new[:10] }}</code></td>{% endfor %}
<td><code>{{ t.sha_old[:12] if t.sha_old else '-' }} -&gt; {{ t.sha_new[:12] if t.sha_new else '-' }}</code></td></tr>
{% endfor %}</table></section>

{% for t in r.tools %}{% for f in t.fields if not f.same %}
<section id="diff"><h2>변경된 필드: {{ t.name }}.{{ f.field }}</h2>
<pre>{% for line in f.diff %}<span class="{{ 'add' if line.startswith('+') and not line.startswith('+++') else ('del' if line.startswith('-') and not line.startswith('---') else 'hdr') }}">{{ line }}</span>
{% endfor %}</pre></section>
{% endfor %}{% endfor %}

<section id="findings"><h2>설명 안 의심 문구</h2>
{% if r.findings %}<table><tr><th>도구</th><th>분류</th><th>찾은 문구</th></tr>
{% for f in r.findings %}<tr><td>{{ f.tool }}</td><td>{{ f.rule }}</td><td><code>{{ f.match }}</code></td></tr>{% endfor %}</table>
{% else %}<p>규칙에 걸린 문구가 없습니다.</p>{% endif %}</section>
</main></html>"""

INDEX = """<!doctype html><meta charset="utf-8"><title>보고서 목록</title>
<h1>보고서 목록</h1><ul>{% for n in names %}<li><a href="/r/{{ n }}">{{ n }}</a></li>{% endfor %}</ul>"""


@app.route("/")
def index():
    return render_template_string(INDEX, names=sorted(p.stem for p in REPORTS.glob("*.json")))


@app.route("/r/<name>")
def show(name):
    path = REPORTS / f"{name}.json"
    if not path.is_file() or "/" in name:
        abort(404)
    return render_template_string(PAGE, r=json.loads(path.read_text(encoding="utf-8")))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
