# 변조 실험용입니다. 실제 증거에는 쓰지 않습니다.
#   python tamper.py file   : 증거 파일의 첫 바이트 1개를 바꿉니다.
#   python tamper.py log    : 기록 2번 줄의 인계 대상 이름을 바꿉니다(해시는 그대로 둡니다).
#   python tamper.py rehash : 기록 2번 줄을 바꾸고 그 줄의 record_hash 도 다시 계산해 맞춥니다.
import hashlib
import json
import sys
from pathlib import Path

mode = sys.argv[1]
if mode == "file":
    p = Path("evidence/disk-image-01.bin")
    data = bytearray(p.read_bytes())
    data[0] ^= 0x01
    p.write_bytes(data)
    print("파일 첫 바이트를 바꿨습니다")
else:
    p = Path("custody.jsonl")
    lines = p.read_text(encoding="utf-8").splitlines()
    rec = json.loads(lines[1])
    rec["to"] = "park"
    if mode == "rehash":
        body = {k: v for k, v in rec.items() if k != "record_hash"}
        data = json.dumps(body, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
        rec["record_hash"] = hashlib.sha256(data.encode("utf-8")).hexdigest()
    lines[1] = json.dumps(rec, ensure_ascii=False)
    p.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print("기록 2번 줄의 to 값을 lee 에서 park 으로 바꿨습니다" + (" (record_hash 도 다시 계산)" if mode == "rehash" else ""))
