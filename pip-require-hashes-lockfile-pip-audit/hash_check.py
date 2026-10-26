"""잠금 파일의 해시와 인덱스가 지금 내주는 파일의 해시를 나란히 비교해 JSON으로 남긴다.

사용법: python hash_check.py 잠금파일 인덱스주소 결과.json
pip install --require-hashes 가 속으로 하는 비교를, 어떤 값이 어긋났는지 보이게 풀어 쓴 것이다.
"""
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

lock, index, out = sys.argv[1:4]

# 잠금 파일에서 "이름==버전"과 그 아래 --hash 줄들을 읽는다.
pins, current = [], None
for line in Path(lock).read_text(encoding="utf-8").splitlines():
    head = re.match(r"^([A-Za-z0-9._-]+)==(\S+)", line)
    if head:
        current = {"name": head.group(1), "version": head.group(2), "locked": []}
        pins.append(current)
    found = re.search(r"--hash=sha256:([0-9a-f]{64})", line)
    if found and current is not None:
        current["locked"].append(found.group(1))

rows = []
for pin in pins:
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(
            [sys.executable, "-m", "pip", "download", "-q", "--no-deps", "--no-cache-dir",
             "-d", tmp, "-i", index, f"{pin['name']}=={pin['version']}"],
            check=True,
        )
        files = [f for f in Path(tmp).iterdir() if f.is_file()]
        actual = hashlib.sha256(files[0].read_bytes()).hexdigest()
        rows.append({
            "name": pin["name"],
            "version": pin["version"],
            "file": files[0].name,
            "locked": pin["locked"],
            "actual": actual,
            "match": actual in pin["locked"],
        })

Path(out).write_text(json.dumps({"index": index, "rows": rows}, indent=2), encoding="utf-8")
for r in rows:
    print(r["name"], r["version"], "일치" if r["match"] else "불일치")
