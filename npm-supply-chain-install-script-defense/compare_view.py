"""results.json 을 읽어 방어 전후 비교 화면(HTML)을 만든다. 사용법: python compare_view.py results.json compare.html"""
import json
import sys

r = json.load(open(sys.argv[1], encoding="utf-8"))
rows = [
    ("npm ci (기본)", r["default"], "설치 중 postinstall 이 실행되어 표시 파일이 생김"),
    ("npm ci --ignore-scripts", r["ignore_scripts"], "설치 스크립트를 건너뜀"),
    ("npm rebuild cr-hook-demo", r["after_rebuild"], "필요한 패키지 하나만 골라 스크립트를 실행"),
]
tr = "".join(
    f"<tr><td><code>{a}</code></td><td style='font-weight:700;color:{'#c62828' if v == '실행됨' else '#1b7f3b'}'>{v}</td><td>{c}</td></tr>"
    for a, v, c in rows
)
open(sys.argv[2], "w", encoding="utf-8").write(f"""<!doctype html><meta charset='utf-8'><title>방어 전후 비교</title>
<style>body{{font:15px 'Malgun Gothic',sans-serif;margin:32px;color:#1f2933}}h1{{font-size:22px;margin:0 0 6px}}
p{{margin:0 0 18px;color:#52606d}}table{{border-collapse:collapse;width:100%}}
th,td{{border:1px solid #d5dbe1;padding:10px 12px;text-align:left}}th{{background:#f1f4f7}}</style>
<h1>설치 방식별 postinstall 실행 여부</h1><p>같은 package-lock.json 으로 cr-hook-demo 의 표시 파일이 생겼는지 확인한 결과입니다.</p>
<table><tr><th>명령</th><th>cr-hook-demo postinstall</th><th>설명</th></tr>{tr}</table>""")
