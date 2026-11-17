"""보관 기록(chain of custody) 도구. 표준 라이브러리만 씁니다.

  python custody.py add <파일> --by 이름 [--note 메모]
  python custody.py handoff <파일> --from 이름 --to 이름 [--note 메모]
  python custody.py verify

기록은 custody.jsonl 에 한 줄에 하나씩 쌓입니다. 각 기록은 앞 기록의 해시(prev)를
포함하고, 자기 해시(record_hash)는 record_hash 를 뺀 나머지 필드로 계산합니다.
"""
import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

LOG = Path("custody.jsonl")
ZERO = "0" * 64


def file_sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def record_hash(rec):
    body = {k: v for k, v in rec.items() if k != "record_hash"}
    data = json.dumps(body, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def read_log():
    if not LOG.exists():
        return []
    return [json.loads(line) for line in LOG.read_text(encoding="utf-8").splitlines() if line.strip()]


def append(action, item, **fields):
    records = read_log()
    rec = {
        "seq": len(records) + 1,
        "time": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "action": action,
        "item": item,
        "sha256": file_sha256(item),
        **fields,
        "prev": records[-1]["record_hash"] if records else ZERO,
    }
    rec["record_hash"] = record_hash(rec)
    with open(LOG, "a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return rec


def cmd_add(a):
    rec = append("add", a.file, by=a.by, note=a.note)
    print(f"#{rec['seq']} add {a.file}\n  sha256 {rec['sha256']}")


def cmd_handoff(a):
    first = next((r for r in read_log() if r["item"] == a.file and r["action"] == "add"), None)
    if first is None:
        sys.exit(f"{a.file}: add 기록이 없습니다")
    rec = append("handoff", a.file, **{"from": a.from_, "to": a.to, "note": a.note})
    print(f"#{rec['seq']} handoff {a.file} {a.from_} -> {a.to}\n  sha256 {rec['sha256']}")
    if rec["sha256"] != first["sha256"]:
        print("  경고: 처음 등록한 해시와 다릅니다")


def cmd_verify(_):
    records = read_log()
    firsts = {}
    for r in records:
        firsts.setdefault(r["item"], r)
    bad = 0
    prev = ZERO
    for r in records:
        if r["seq"] != records.index(r) + 1:
            print(f"#{r['seq']} 순번이 맞지 않습니다")
            bad += 1
        if r["prev"] != prev:
            print(f"#{r['seq']} 체인 끊김: prev 가 앞 기록의 record_hash 와 다릅니다")
            bad += 1
        elif record_hash(r) != r["record_hash"]:
            print(f"#{r['seq']} 기록 변조: 내용으로 계산한 해시가 record_hash 와 다릅니다")
            bad += 1
        else:
            print(f"#{r['seq']} 기록 체인 정상")
        if r["sha256"] != firsts[r["item"]]["sha256"]:
            print(f"#{r['seq']} 이 기록의 파일 해시가 등록 시점과 다릅니다 ({r['time']})")
            bad += 1
        prev = r["record_hash"]
    for item, first in firsts.items():
        if not Path(item).exists():
            print(f"{item} 파일 없음")
            bad += 1
            continue
        now = file_sha256(item)
        if now == first["sha256"]:
            print(f"{item} 파일 해시 일치")
        else:
            print(f"{item} 파일 해시 불일치: 등록 {first['sha256'][:16]}... / 현재 {now[:16]}...")
            bad += 1
    print("검증 실패" if bad else "검증 통과")
    sys.exit(1 if bad else 0)


ap = argparse.ArgumentParser()
sub = ap.add_subparsers(dest="cmd", required=True)
p = sub.add_parser("add")
p.add_argument("file")
p.add_argument("--by", required=True)
p.add_argument("--note", default="")
p.set_defaults(fn=cmd_add)
p = sub.add_parser("handoff")
p.add_argument("file")
p.add_argument("--from", dest="from_", required=True)
p.add_argument("--to", required=True)
p.add_argument("--note", default="")
p.set_defaults(fn=cmd_handoff)
p = sub.add_parser("verify")
p.set_defaults(fn=cmd_verify)
args = ap.parse_args()
args.fn(args)
