"""에이전트 규칙 파일(AGENTS.md 등)에 숨은 지시를 찾는 정적 스캐너. 표준 라이브러리만 씁니다.

사용법: python agent_config_scan.py <파일 또는 폴더>... [--json] [--html 보고서.html] [--fail-on high|any]
종료 코드: 0 = 통과, 1 = 게이트 실패(발견 있음), 2 = 사용 오류
"""
import argparse
import base64
import binascii
import html
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

NAMES = {"agents.md", "claude.md", "gemini.md", ".cursorrules", ".windsurfrules", ".clinerules",
         "copilot-instructions.md"}
SKIP_DIRS = {".git", "node_modules", ".venv", "__pycache__"}

ZERO = {0x200B, 0x200C, 0x200D, 0x2060, 0xFEFF, 0x180E}
BIDI = set(range(0x202A, 0x202F)) | set(range(0x2066, 0x206A)) | {0x200E, 0x200F, 0x061C}
TAGS = range(0xE0000, 0xE0080)

SUSPECT_COMMENT = re.compile(
    r"ignore|disregard|instruction|system prompt|do not (tell|mention|reveal)|don't (tell|mention)|"
    r"secret|override|curl|wget|exec|send|upload|지시|무시|몰래|알리지|전송|실행|비밀", re.I)
NET = re.compile(r"\b(curl|wget|Invoke-WebRequest|iwr|nc|netcat|scp)\b", re.I)
SENSITIVE = re.compile(r"\$\(\s*env\s*\)|\bprintenv\b|\benv\b|\.env\b|secret|token|api[_-]?key|password|"
                       r"credential|환경\s*변수|비밀|토큰|\.ssh|id_rsa", re.I)
B64 = re.compile(r"(?<![A-Za-z0-9+/=])[A-Za-z0-9+/]{40,}={0,2}(?![A-Za-z0-9+/=])")


@dataclass
class Finding:
    file: str
    line: int
    col: int
    kind: str
    severity: str   # "높음" 또는 "확인"
    detail: str
    restored: str


def is_agent_file(path):
    name = path.name.lower()
    if name in NAMES or name.endswith(".instructions.md"):
        return True
    return name.endswith(".mdc") and ".cursor" in [p.lower() for p in path.parts]


def collect(paths):
    files = []
    for p in map(Path, paths):
        if p.is_dir():
            for f in sorted(p.rglob("*")):
                if f.is_file() and is_agent_file(f) and not SKIP_DIRS & set(f.parts):
                    files.append(f)
        elif p.is_file():
            files.append(p)   # 파일을 직접 받으면 이름과 상관없이 검사합니다(pre-commit 용)
        else:
            raise FileNotFoundError(p)
    return files


def hidden_class(ch):
    cp = ord(ch)
    if cp in TAGS:
        return "tag"
    if cp in BIDI:
        return "bidi"
    if cp in ZERO:
        return "zero"
    return ""


def show(text):
    """숨은 문자를 <U+XXXX> 로 바꿔 눈에 보이게 합니다."""
    return "".join(f"<U+{ord(c):04X}>" if hidden_class(c) else c for c in text)


def restore(run, line):
    classes = {hidden_class(c) for c in run}
    if "tag" in classes:
        text = "".join(chr(ord(c) - 0xE0000) for c in run if 0x20 <= ord(c) - 0xE0000 < 0x7F)
        return "tag", text
    if classes == {"zero"} and {ord(c) for c in run} <= {0x200B, 0x200C} and len(run) % 8 == 0:
        bits = "".join("0" if c == "\u200b" else "1" for c in run)
        try:
            return "zero", bytes(int(bits[i:i + 8], 2) for i in range(0, len(bits), 8)).decode("utf-8")
        except UnicodeDecodeError:
            pass
    return ("bidi" if "bidi" in classes else "zero"), show(line.strip())[:100]


def allowed(run, before, after, lineno, col):
    """정상적으로 쓰이는 경우를 거릅니다. 한계는 본문에 적었습니다."""
    if run == "\ufeff" and lineno == 1 and col == 0:
        return True                      # 파일 맨 앞의 BOM
    if run in ("\u200c", "\u200d") and before and after and ord(before) > 127 and ord(after) > 127:
        return True                      # 이모지 결합, 한글 등 비ASCII 글자 사이
    if before == "\U0001F3F4" and all(ord(c) in TAGS for c in run):
        return True                      # 깃발 이모지 뒤의 태그 문자
    return False


def scan_text(name, text):
    out = []
    for lineno, line in enumerate(text.split("\n"), 1):
        i = 0
        while i < len(line):
            if not hidden_class(line[i]):
                i += 1
                continue
            j = i
            while j < len(line) and hidden_class(line[j]):
                j += 1
            run = line[i:j]
            before = line[i - 1] if i else ""
            after = line[j] if j < len(line) else ""
            if not allowed(run, before, after, lineno, i):
                kind, restored = restore(run, line)
                label = {"tag": "숨은 유니코드(태그 문자)", "zero": "숨은 유니코드(제로폭)",
                         "bidi": "숨은 유니코드(양방향 제어)"}[kind]
                out.append(Finding(name, lineno, i + 1, label, "높음",
                                   f"U+{ord(run[0]):04X} 포함 {len(run)}자", restored))
            i = j
        net = NET.search(line)
        if net and SENSITIVE.search(line):
            out.append(Finding(name, lineno, net.start() + 1, "외부 전송 명령 문구", "높음", net.group(0),
                               show(line.strip())[:100]))
        elif net and re.search(r"https?://", line):
            out.append(Finding(name, lineno, net.start() + 1, "네트워크 명령 문구", "확인", net.group(0),
                               show(line.strip())[:100]))
        for m in B64.finditer(line):
            if re.fullmatch(r"[0-9a-fA-F]+", m.group(0)):
                continue                 # 커밋 해시 같은 16진수는 제외
            try:
                raw = base64.b64decode(m.group(0) + "=" * (-len(m.group(0)) % 4), validate=True)
                decoded = raw.decode("utf-8")
            except (binascii.Error, UnicodeDecodeError):
                continue
            if len(decoded) >= 8 and sum(c.isprintable() for c in decoded) / len(decoded) >= 0.95:
                out.append(Finding(name, lineno, m.start() + 1, "base64 덩어리", "높음",
                                   f"{len(m.group(0))}자", decoded))
    for m in re.finditer(r"<!--(.*?)-->", text, re.S):
        body = " ".join(m.group(1).split())
        if SUSPECT_COMMENT.search(body):
            lineno = text.count("\n", 0, m.start()) + 1
            out.append(Finding(name, lineno, 1, "HTML 주석 속 지시", "높음", f"{len(body)}자", body[:100]))
    return sorted(out, key=lambda f: (f.line, f.col))


def scan(paths):
    files = collect(paths)
    findings = []
    for f in files:
        findings += scan_text(str(f).replace("\\", "/"), f.read_text(encoding="utf-8", errors="replace"))
    return files, findings


def gate_failed(findings, fail_on="high"):
    if fail_on == "any":
        return bool(findings)
    return any(f.severity == "높음" for f in findings)


def render_html(files, findings, fail_on="high"):
    failed = gate_failed(findings, fail_on)
    rows = "".join(
        f"<tr class='{'hi' if f.severity == '높음' else 'chk'}'><td>{f.severity}</td><td>{html.escape(f.file)}</td>"
        f"<td>{f.line}:{f.col}</td><td>{html.escape(f.kind)}</td><td>{html.escape(f.detail)}</td>"
        f"<td><code>{html.escape(f.restored)}</code></td></tr>" for f in findings)
    table = ("<table><tr><th>등급</th><th>파일</th><th>줄:칸</th><th>유형</th><th>내용</th><th>복원한 숨은 내용</th></tr>"
             + rows + "</table>") if findings else "<p>발견된 항목이 없습니다.</p>"
    verdict = (f"게이트 실패 (종료 코드 1): {len(findings)}건 발견" if failed
               else f"게이트 통과 (종료 코드 0): 검사 {len(files)}개 파일" + (f", 확인 {len(findings)}건" if findings else ""))
    names = ", ".join(html.escape(str(f).replace("\\", "/")) for f in files)
    return (f"<!doctype html><html lang='ko'><meta charset='utf-8'><title>규칙 파일 스캔 보고서</title><style>"
            "body{font-family:'Malgun Gothic',sans-serif;margin:0;background:#f4f5f7;color:#1f2933}"
            "header{background:#1f2933;color:#fff;padding:14px 28px;font-size:18px}main{padding:20px 28px}"
            ".v{font-size:20px;padding:12px 16px;border-radius:8px;margin-bottom:16px}"
            ".v.f{background:#fde7e4;border:1px solid #b42318}.v.p{background:#e3f6ec;border:1px solid #067647}"
            "table{border-collapse:collapse;width:100%;background:#fff}td,th{border:1px solid #d5d9de;padding:6px 10px;"
            "text-align:left;font-size:14px;vertical-align:top}th{background:#e4e7eb}tr.hi td:first-child{color:#b42318;"
            "font-weight:700}tr.chk td:first-child{color:#8a5a00;font-weight:700}code{word-break:break-all}"
            f"</style><header>에이전트 규칙 파일 스캔 보고서</header><main><div class='v {'f' if failed else 'p'}'>{verdict}</div>"
            f"<p>검사한 파일 {len(files)}개: {names}</p>{table}</main></html>")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--html")
    ap.add_argument("--fail-on", choices=["high", "any"], default="high")
    args = ap.parse_args()
    try:
        files, findings = scan(args.paths)
    except FileNotFoundError as e:
        print(f"경로를 찾을 수 없습니다: {e}", file=sys.stderr)
        return 2
    if args.html:
        Path(args.html).write_text(render_html(files, findings, args.fail_on), encoding="utf-8")
    if args.json:
        print(json.dumps([asdict(f) for f in findings], ensure_ascii=False, indent=2))
    else:
        for f in findings:
            print(f"[{f.severity}] {f.file}:{f.line}:{f.col}  {f.kind}  {f.detail}")
            print(f"        복원: {f.restored}")
        high = sum(f.severity == "높음" for f in findings)
        print(f"검사 {len(files)}개 파일, 발견 {len(findings)}건 (높음 {high}, 확인 {len(findings) - high})")
    return 1 if gate_failed(findings, args.fail_on) else 0


if __name__ == "__main__":
    sys.exit(main())
