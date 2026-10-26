"""잠금 파일을 일부러 망가뜨린 연습용 사본 두 개를 만든다.

requirements.bad.lock    : requests 의 해시 각각의 마지막 한 글자를 바꾼다.
requirements.nohash.lock : idna 의 해시 줄을 지워 해시 없는 의존성을 섞는다.
"""
import re
from pathlib import Path

lines = Path("requirements.lock").read_text(encoding="utf-8").splitlines()
HASH = re.compile(r"(--hash=sha256:[0-9a-f]{63})([0-9a-f])")


def flip(m):
    return m.group(1) + ("0" if m.group(2) != "0" else "1")


bad, nohash, current = [], [], ""
for ln in lines:
    head = re.match(r"^([A-Za-z0-9._-]+)==", ln)
    if head:
        current = head.group(1).lower()
    bad.append(HASH.sub(flip, ln) if current == "requests" else ln)
    if current == "idna" and "--hash=sha256:" in ln:
        continue
    # idna 줄 끝의 이어쓰기 문자(역슬래시)도 함께 뗀다
    nohash.append(ln[:-2] if current == "idna" and ln.startswith("idna==") else ln)

Path("requirements.bad.lock").write_text("\n".join(bad) + "\n", encoding="utf-8", newline="\n")
Path("requirements.nohash.lock").write_text("\n".join(nohash) + "\n", encoding="utf-8", newline="\n")
print("만든 파일: requirements.bad.lock, requirements.nohash.lock")
