"""package-lock.json 두 개를 비교해 위험한 변경을 HTML 보고서로 만든다.

사용법: python lockdiff.py 이전.json 이후.json 허용레지스트리주소 보고서.html
종료 코드: 높음 등급이 하나라도 있으면 1, 없으면 0.
"""
import html
import json
import sys
from urllib.parse import urlparse


def load(path):
    data = json.load(open(path, encoding="utf-8"))
    return {k: v for k, v in data["packages"].items() if k}


def origin(url):
    u = urlparse(url)
    return f"{u.scheme}://{u.netloc}"


def tail(value):
    return "끝 " + value[-16:]


def compare(old, new, allowed):
    findings = []  # (등급, 패키지, 항목, 이전, 이후)
    for key, n in sorted(new.items()):
        name = key.split("node_modules/")[-1]
        o = old.get(key)
        res = n.get("resolved", "")
        if res and origin(res) != allowed:
            findings.append(("높음", name, "예상 밖 레지스트리", origin(allowed), origin(res)))
        if o is None:
            findings.append(("정보", name, "새 의존성", "-", n.get("version", "")))
            if n.get("hasInstallScript"):
                findings.append(("주의", name, "새 의존성이 설치 스크립트 보유", "-", "hasInstallScript"))
            continue
        same_version = o.get("version") == n.get("version")
        if o.get("integrity") != n.get("integrity"):
            if same_version:
                findings.append(("높음", name, "같은 버전인데 integrity 변경",
                                 tail(o.get("integrity", "")), tail(n.get("integrity", ""))))
            else:
                findings.append(("정보", name, "버전 변경으로 integrity 변경",
                                 o.get("version", ""), n.get("version", "")))
        if o.get("resolved") != n.get("resolved") and same_version:
            findings.append(("높음", name, "같은 버전인데 resolved 변경", o.get("resolved", ""), res))
        if n.get("hasInstallScript") and not o.get("hasInstallScript"):
            findings.append(("주의", name, "설치 스크립트가 새로 생김", "없음", "hasInstallScript"))
    for key in sorted(set(old) - set(new)):
        findings.append(("정보", key.split("node_modules/")[-1], "의존성 제거", old[key].get("version", ""), "-"))
    return findings


def render(findings, allowed):
    color = {"높음": "#c62828", "주의": "#b26a00", "정보": "#52606d"}
    rows = "".join(
        f"<tr><td style='color:{color[g]};font-weight:700'>{g}</td><td>{html.escape(p)}</td>"
        f"<td>{html.escape(i)}</td><td><code>{html.escape(a)}</code></td><td><code>{html.escape(b)}</code></td></tr>"
        for g, p, i, a, b in findings
    )
    high = sum(1 for f in findings if f[0] == "높음")
    warn = sum(1 for f in findings if f[0] == "주의")
    return f"""<!doctype html><meta charset='utf-8'><title>락파일 변경 보고서</title>
<style>body{{font:15px 'Malgun Gothic',sans-serif;margin:32px;color:#1f2933}}
h1{{font-size:22px;margin:0 0 6px}}p{{margin:0 0 18px;color:#52606d}}
table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #d5dbe1;padding:8px 10px;text-align:left;vertical-align:top}}
th{{background:#f1f4f7;white-space:nowrap}}code{{font-size:12.5px;word-break:break-all}}</style>
<h1>락파일 변경 보고서: 높음 {high}건, 주의 {warn}건</h1>
<p>허용 레지스트리 {html.escape(allowed)}</p>
<table><tr><th>등급</th><th>패키지</th><th>항목</th><th>이전</th><th>이후</th></tr>{rows}</table>"""


if __name__ == "__main__":
    old_path, new_path, allowed, out = sys.argv[1:5]
    found = compare(load(old_path), load(new_path), allowed.rstrip("/"))
    open(out, "w", encoding="utf-8").write(render(found, allowed))
    for f in found:
        print(" | ".join(f))
    sys.exit(1 if any(f[0] == "높음" for f in found) else 0)
