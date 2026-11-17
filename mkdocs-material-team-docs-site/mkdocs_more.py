"""MkDocs Material 심화: 확장 기능(경고 상자, 탭, 접기, 코드 복사), 밝은/어두운 테마, 검색 색인, 엄격 빌드가 잡는 오류, 화면 캡처.

준비: pip install mkdocs mkdocs-material playwright (그리고 크롬 또는 playwright install chromium)
주의: 임시 폴더에 프로젝트를 만들어 빌드하고 끝에서 지운다. 화면 캡처는 이 PC의 127.0.0.1:8765 에 잠깐 서버를 띄운다.
실행: python -X utf8 mkdocs_more.py [캡처를 저장할 폴더]   (약 40초)
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import threading
import functools
import http.server

from playwright.sync_api import sync_playwright

SHOTS = sys.argv[1] if len(sys.argv) > 1 else None
root = tempfile.mkdtemp(prefix="mk-")
os.makedirs(os.path.join(root, "docs", "ops"))

CFG = """site_name: Team Notes
theme:
  name: material
  language: ko
  palette:
    - media: "(prefers-color-scheme: light)"
      scheme: default
      toggle: {icon: material/weather-night, name: 어두운 테마로}
    - media: "(prefers-color-scheme: dark)"
      scheme: slate
      toggle: {icon: material/weather-sunny, name: 밝은 테마로}
  features: [content.code.copy, navigation.sections, search.suggest, toc.follow]
nav:
  - 처음: index.md
  - 운영:
      - 배포 절차: ops/deploy.md
      - 장애 대응: ops/runbook.md
markdown_extensions:
  - admonition
  - tables
  - toc: {permalink: true}
  - pymdownx.details
  - pymdownx.superfences
  - pymdownx.tabbed: {alternate_style: true}
validation:
  anchors: warn
"""
INDEX = """# 팀 문서

!!! note "이 문서는"
    팀 운영 절차를 모아 둡니다. 수정은 `docs/` 폴더의 마크다운을 고치면 됩니다.

!!! warning "주의"
    운영 서버에서 직접 명령을 실행하기 전에 [배포 절차](ops/deploy.md)를 먼저 읽습니다.

??? tip "접어 둔 설명(눌러서 펼침)"
    자주 묻는 질문은 이곳에 모읍니다.

=== "리눅스"
    ```bash
    sudo systemctl restart app
    ```
=== "윈도우"
    ```powershell
    Restart-Service app
    ```

| 구분 | 담당 | 연락 |
|---|---|---|
| 배포 | 운영팀 | 내선 101 |
| 장애 | 보안팀 | 내선 202 |
"""
DEPLOY = "# 배포 절차\n\n## 준비\n\n1. 변경 내용을 확인합니다.\n\n## 실행\n\n명령을 실행합니다.\n"
RUNBOOK = "# 장애 대응\n\n[배포 절차의 실행 단계](deploy.md#실행)를 따릅니다.\n"
for name, text in (("mkdocs.yml", CFG), ("docs/index.md", INDEX), ("docs/ops/deploy.md", DEPLOY), ("docs/ops/runbook.md", RUNBOOK)):
    open(os.path.join(root, name), "w", encoding="utf-8", newline="\n").write(text)


def mk(*a):
    r = subprocess.run([sys.executable, "-X", "utf8", "-m", "mkdocs", *a], cwd=root, capture_output=True, text=True, encoding="utf-8")
    return r.returncode, (r.stdout + r.stderr)


print("## 1. 엄격 빌드(--strict)")
code, out = mk("build", "--strict", "--quiet")
print(f"  종료 코드 {code}", "(경고도 오류로 보는 상태에서 통과)" if code == 0 else out[:200])

site = os.path.join(root, "site")
files = [os.path.join(d, f) for d, _, fs in os.walk(site) for f in fs]
size = sum(os.path.getsize(f) for f in files)
idx = json.load(open(os.path.join(site, "search", "search_index.json"), encoding="utf-8"))
html = open(os.path.join(site, "index.html"), encoding="utf-8").read()
print(f"\n## 2. 빌드 결과: 파일 {len(files)}개, 합계 {size / 1024:.0f}KB, 검색 색인 항목 {len(idx['docs'])}개")
print(f"  경고 상자 {html.count('class=\"admonition')}개, 접기 {html.count('<details')}개, 탭 묶음 {html.count('tabbed-set')}개")
print(f"  밝은/어두운 테마 표시: scheme 값 {sorted(set(__import__('re').findall(r'data-md-color-scheme=\"(\w+)\"', html)))}")

print("\n## 3. 일부러 망가뜨린 세 가지를 --strict 가 잡는가")
cases = {
    "없는 페이지로 링크": ("docs/ops/runbook.md", "# 장애 대응\n\n[없는 글](nothing.md)\n"),
    "없는 제목(#앵커)으로 링크": ("docs/ops/runbook.md", "# 장애 대응\n\n[배포](deploy.md#없는제목)\n"),
    "nav 에 없는 파일 이름": ("mkdocs.yml", CFG.replace("ops/runbook.md", "ops/missing.md")),
}
good_runbook = RUNBOOK
for label, (path, text) in cases.items():
    open(os.path.join(root, path), "w", encoding="utf-8", newline="\n").write(text)
    code, out = mk("build", "--strict")
    line = next((l for l in out.splitlines() if "WARNING" in l or "ERROR" in l or "Aborted" in l), "").strip()
    print(f"  {label:<24} 종료 코드 {code} | {line[:70]}")
    if label.startswith("없는 페이지"):
        code_q, _ = mk("build", "--strict", "--quiet")
        print(f"    같은 오류에 --quiet 을 더하면 종료 코드 {code_q} (경고가 숨겨져 엄격 검사가 통과해 버림)")
    open(os.path.join(root, "docs/ops/runbook.md"), "w", encoding="utf-8", newline="\n").write(good_runbook)
    open(os.path.join(root, "mkdocs.yml"), "w", encoding="utf-8", newline="\n").write(CFG)

print("\n## 4. 화면 캡처(밝은 테마와 어두운 테마)")
mk("build", "--quiet")
class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


handler = functools.partial(Quiet, directory=site)
srv = http.server.ThreadingHTTPServer(("127.0.0.1", 8765), handler)
threading.Thread(target=srv.serve_forever, daemon=True).start()
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True)
    for scheme in ("light", "dark"):
        pg = b.new_page(viewport={"width": 1100, "height": 760}, color_scheme=scheme)
        pg.goto("http://127.0.0.1:8765/", wait_until="load")
        pg.wait_for_timeout(800)
        got = pg.evaluate("document.body.getAttribute('data-md-color-scheme')")
        if SHOTS:
            os.makedirs(SHOTS, exist_ok=True)
            pg.screenshot(path=os.path.join(SHOTS, f"{'03' if scheme == 'light' else '04'}-페이지-{scheme}.png"))
        print(f"  브라우저 선호 {scheme:<5} -> 페이지의 data-md-color-scheme = {got}")
    b.close()
srv.shutdown()
shutil.rmtree(root, ignore_errors=True)
print("  임시 폴더와 서버 정리 완료")
