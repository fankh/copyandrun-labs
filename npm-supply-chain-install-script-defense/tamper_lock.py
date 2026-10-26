"""실습용: 잠금 파일에서 cr-hook-demo 항목의 주소와 해시를 일부러 바꿔 변조된 사본을 만든다."""
import json
import sys

src, dst = sys.argv[1:3]
lock = json.load(open(src, encoding="utf-8"))
entry = lock["packages"]["node_modules/cr-hook-demo"]
entry["resolved"] = entry["resolved"].replace("127.0.0.1:14873", "127.0.0.1:14999")
integ = entry["integrity"]
entry["integrity"] = integ[:-3] + ("AAA" if not integ.endswith("AAA") else "BBB")
json.dump(lock, open(dst, "w", encoding="utf-8"), indent=2)
