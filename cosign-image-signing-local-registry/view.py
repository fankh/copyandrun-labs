"""검증 결과를 표로 보여 주는 작은 웹 화면. 게이트 스크립트를 그대로 호출합니다."""
import html
import os
import shutil
import subprocess
import urllib.request
from pathlib import Path

from flask import Flask

HERE = Path(__file__).resolve().parent
REGISTRY = "localhost:5390"
REPO = "demo/hello"
MANIFEST_TYPES = ",".join([
    "application/vnd.oci.image.index.v1+json",
    "application/vnd.oci.image.manifest.v1+json",
    "application/vnd.docker.distribution.manifest.list.v2+json",
    "application/vnd.docker.distribution.manifest.v2+json",
])

app = Flask(__name__)


def tag_digest(tag):
    req = urllib.request.Request(
        f"http://{REGISTRY}/v2/{REPO}/manifests/{tag}",
        method="HEAD", headers={"Accept": MANIFEST_TYPES})
    try:
        with urllib.request.urlopen(req, timeout=5) as r:
            return r.headers["Docker-Content-Digest"]
    except OSError:
        return "-"


def run_gate(ref, sbom=False):
    env = {"REQUIRE_SBOM": "1" if sbom else "0"}
    p = subprocess.run([shutil.which("bash"), str(HERE / "verify_gate.sh"), ref],
                       capture_output=True, text=True, timeout=120, env={**os.environ, **env})
    return p.returncode, (p.stdout + p.stderr).strip()


@app.get("/")
def index():
    signed = (HERE / "signed.digest").read_text().strip()
    rows = [
        ("태그 1.0", f"{REGISTRY}/{REPO}:1.0", tag_digest("1.0"), False),
        ("다이제스트 고정", f"{REGISTRY}/{REPO}@{signed}", signed, True),
        ("태그 2.0 (서명 안 함)", f"{REGISTRY}/{REPO}:2.0", tag_digest("2.0"), False),
    ]
    body = []
    for label, ref, digest, sbom in rows:
        code, out = run_gate(ref, sbom)
        ok = code == 0
        same = "같음" if digest == signed else "다름"
        body.append(
            f"<tr><td>{html.escape(label)}</td>"
            f"<td><code>{html.escape(digest[:19])}...</code></td><td>{same}</td>"
            f"<td class='{'ok' if ok else 'bad'}'>{'통과' if ok else '거부'}</td>"
            f"<td>{code}</td></tr>")
    return f"""<!doctype html><meta charset="utf-8"><title>서명 검증 결과</title>
<style>
body{{font-family:'Malgun Gothic',sans-serif;margin:32px;color:#222}}
table{{border-collapse:collapse;min-width:760px}}
th,td{{border:1px solid #ccc;padding:9px 14px;text-align:left}}
th{{background:#f2f4f7}} .ok{{background:#dff5e1;color:#14692a;font-weight:700}}
.bad{{background:#fde1e1;color:#a11919;font-weight:700}} code{{font-size:13px}}
</style>
<h1>배포 전 서명 검증</h1>
<p>서명한 다이제스트: <code>{html.escape(signed[:19])}...</code></p>
<table><tr><th>대상</th><th>지금 가리키는 다이제스트</th><th>서명한 것과</th><th>게이트</th><th>종료 코드</th></tr>
{''.join(body)}</table>"""


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5392)
