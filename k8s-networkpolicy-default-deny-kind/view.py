"""파드 사이 연결 결과를 표로 보여 주는 점검 화면.
- python view.py          : 브라우저용 화면 (http://127.0.0.1:5420)
- python view.py --text   : 같은 표를 터미널에 출력
각 칸은 출발 파드 안에서 wget 으로 대상에 연결해 본 실제 결과입니다."""
import html
import subprocess
import sys
import unicodedata
from concurrent.futures import ThreadPoolExecutor

from flask import Flask

# (설명, 출발 네임스페이스, 출발 파드, 대상 주소, 수정 후 기대)
CASES = [
    ("outside 의 client -> web", "outside", "client", "web.shop:8080", True),
    ("web -> db", "shop", "web", "db.shop:5432", True),
    ("intruder -> db", "shop", "intruder", "db.shop:5432", False),
    ("intruder -> web", "shop", "intruder", "web.shop:8080", False),
    ("web -> intruder", "shop", "web", "intruder.shop:8080", False),
    ("outside 의 client -> db", "outside", "client", "db.shop:5432", False),
]

app = Flask(__name__)


def kubectl(*args, timeout=30):
    p = subprocess.run(["kubectl", *args], capture_output=True, text=True, timeout=timeout)
    return p.returncode, (p.stdout + p.stderr).strip()


def probe(ns, pod, target):
    code, out = kubectl("exec", "-n", ns, pod, "--", "timeout", "4", "wget", "-T", "2", "-qO-", f"http://{target}/", timeout=30)
    return code == 0, out.splitlines()[0] if out else ""


def run_all():
    with ThreadPoolExecutor(max_workers=len(CASES)) as pool:
        results = list(pool.map(lambda c: probe(c[1], c[2], c[3]), CASES))
    return [(label, target, ok, expect, body)
            for (label, _, _, target, expect), (ok, body) in zip(CASES, results)]


def pad(text, width):
    """한글은 두 칸을 차지하므로 화면 너비를 기준으로 맞춥니다."""
    used = sum(2 if unicodedata.east_asian_width(c) in "WF" else 1 for c in text)
    return text + " " * max(width - used, 0)


def text_table(rows):
    widths = (28, 22, 8, 14)
    head = ("경로", "대상", "결과", "수정 후 기대")
    lines = [" | ".join(pad(h, w) for h, w in zip(head, widths)) + " | 판정"]
    for label, target, ok, expect, _ in rows:
        cells = (label, target, "연결됨" if ok else "차단", "허용" if expect else "차단")
        lines.append(" | ".join(pad(c, w) for c, w in zip(cells, widths)) + (" | 일치" if ok == expect else " | 불일치"))
    return "\n".join(lines)


@app.get("/")
def index():
    rows = run_all()
    _, pols = kubectl("get", "networkpolicy", "-n", "shop", "--no-headers", "-o", "custom-columns=NAME:.metadata.name,POD:.spec.podSelector.matchLabels")
    _, pods = kubectl("get", "pods", "-A", "-o", "wide", "--no-headers",
                      "--field-selector", "metadata.namespace!=kube-system,metadata.namespace!=local-path-storage")
    body = []
    for label, target, ok, expect, _ in rows:
        match = ok == expect
        body.append(
            f"<tr><td>{html.escape(label)}</td><td><code>{html.escape(target)}</code></td>"
            f"<td class='{'open' if ok else 'shut'}'>{'연결됨' if ok else '차단'}</td>"
            f"<td>{'허용' if expect else '차단'}</td>"
            f"<td class='{'ok' if match else 'bad'}'>{'일치' if match else '불일치'}</td></tr>")
    bad = sum(1 for r in rows if r[2] != r[3])
    summary = "모든 경로가 기대와 같습니다." if bad == 0 else f"기대와 다른 경로가 {bad}개 있습니다."
    return f"""<!doctype html><meta charset="utf-8"><title>파드 연결 점검</title>
<style>
body{{font-family:'Malgun Gothic',sans-serif;margin:28px;color:#222}}
table{{border-collapse:collapse;min-width:820px;margin-bottom:18px}}
th,td{{border:1px solid #ccc;padding:8px 14px;text-align:left}}
th{{background:#f2f4f7}} .open{{color:#0b5cad;font-weight:700}} .shut{{color:#444;font-weight:700}}
.ok{{background:#dff5e1;color:#14692a;font-weight:700}} .bad{{background:#fde1e1;color:#a11919;font-weight:700}}
pre{{background:#f6f8fa;padding:10px 14px;font-size:13px;border:1px solid #ddd}}
</style>
<h1>파드 사이 연결 점검</h1>
<p><b>{html.escape(summary)}</b> 수정 후 기대는 web 만 db 에 닿고, outside 에서는 web 의 8080 만 열리는 상태입니다.</p>
<table><tr><th>경로</th><th>대상</th><th>지금 결과</th><th>수정 후 기대</th><th>판정</th></tr>{''.join(body)}</table>
<h3>파드</h3><pre>{html.escape(pods)}</pre>
<h3>shop 의 NetworkPolicy ({len(pols.splitlines()) if pols.strip() else 0}개)</h3><pre>{html.escape(pols) if pols.strip() else '없음'}</pre>"""


if __name__ == "__main__":
    if "--text" in sys.argv:
        print(text_table(run_all()))
    else:
        app.run(host="127.0.0.1", port=5420)
