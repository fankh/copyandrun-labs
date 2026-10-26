"""MCP 도구 정의 고정(pin) 및 점검 스크립트.

  python pin_check.py pin   server.py [--pins pins.json]
  python pin_check.py check server.py [--pins pins.json] [--report reports/mismatch.json]

tools/list 로 받은 도구의 이름, 설명, 입력 스키마를 정규화해 SHA-256 으로 고정합니다.
점검할 때 해시가 다르면 어떤 도구의 어느 필드가 바뀌었는지 diff 와 함께 알리고 종료 코드 1 로 끝납니다.
해시가 같아도 설명 안에 의심 문구가 있으면 종료 코드 2 로 끝납니다.
"""
import argparse
import asyncio
import difflib
import hashlib
import json
import os
import re
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

FIELDS = ("name", "description", "inputSchema")

# 의심 문구 규칙: (분류, 정규식)
RULES = [
    ("명령형 지시", re.compile(r"(<IMPORTANT>|하십시오|하세요|하라\b|말하지 마|ignore (all|previous))", re.I)),
    ("민감 경로", re.compile(r"(~/\.\w+|/etc/\w+|\.env\b|id_rsa|\.aws\b)")),
    ("외부 전송", re.compile(r"(https?://\S+|보내십시오|전송|upload|curl )", re.I)),
]


async def fetch_tools(server):
    params = StdioServerParameters(command=sys.executable, args=[server])
    # 서버가 stderr 로 남기는 로그는 점검 출력에 섞이지 않게 버립니다.
    with open(os.devnull, "w") as errlog:
        async with stdio_client(params, errlog=errlog) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                result = await session.list_tools()
    tools = []
    for t in result.tools:
        raw = t.model_dump(mode="json", exclude_none=True)
        tools.append({f: raw.get(f) for f in FIELDS})
    return tools


def normalize(field, value):
    """같은 내용이면 같은 문자열이 되도록 다듬습니다."""
    if field == "inputSchema":
        return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    text = unicodedata.normalize("NFC", value or "").replace("\r\n", "\n")
    return "\n".join(line.rstrip() for line in text.split("\n")).strip()


def sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def snapshot(tools):
    snap = {}
    for t in tools:
        norm = {f: normalize(f, t[f]) for f in FIELDS}
        snap[t["name"]] = {
            "fields": norm,
            "hashes": {f: sha(v) for f, v in norm.items()},
            "sha256": sha(json.dumps(norm, sort_keys=True, ensure_ascii=False)),
        }
    return snap


def scan(snap):
    findings = []
    for name, tool in snap.items():
        for category, pattern in RULES:
            for m in pattern.finditer(tool["fields"]["description"]):
                findings.append({"tool": name, "rule": category, "match": m.group(0)})
    return findings


def pretty(field, text):
    if field == "inputSchema":
        return json.dumps(json.loads(text), sort_keys=True, indent=2, ensure_ascii=False)
    return text


def diff_lines(field, old, new):
    return list(difflib.unified_diff(
        pretty(field, old).splitlines(), pretty(field, new).splitlines(),
        "고정한 값", "현재 값", lineterm="", n=1))


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["pin", "check"])
    ap.add_argument("server")
    ap.add_argument("--pins", default="pins.json")
    ap.add_argument("--report")
    args = ap.parse_args()

    current = snapshot(asyncio.run(fetch_tools(args.server)))
    findings = scan(current)

    if args.mode == "pin":
        data = {"server": args.server, "pinned_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "tools": current}
        Path(args.pins).write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"고정 완료: 도구 {len(current)}개를 {args.pins} 에 저장했습니다.")
        for name, tool in current.items():
            print(f"  {name}  {tool['sha256'][:16]}")
        for f in findings:
            print(f"  경고: {f['tool']} 설명에 [{f['rule']}] {f['match']!r}")
        return

    pinned = json.loads(Path(args.pins).read_text(encoding="utf-8"))["tools"]
    report_tools, changed = [], False
    for name in sorted(set(pinned) | set(current)):
        old, new = pinned.get(name), current.get(name)
        if old is None or new is None:
            changed = True
            status = "새 도구" if old is None else "사라진 도구"
            print(f"변경: {name}  {status}")
            report_tools.append({"name": name, "status": status, "fields": [],
                                 "sha_old": old and old["sha256"], "sha_new": new and new["sha256"]})
            continue
        fields, tool_changed = [], False
        for f in FIELDS:
            same = old["hashes"][f] == new["hashes"][f]
            entry = {"field": f, "same": same, "sha_old": old["hashes"][f], "sha_new": new["hashes"][f], "diff": []}
            if not same:
                tool_changed = True
                entry["diff"] = diff_lines(f, old["fields"][f], new["fields"][f])
                print(f"변경: {name}.{f}  {old['hashes'][f][:12]} -> {new['hashes'][f][:12]}")
                print("\n".join("    " + line for line in entry["diff"]))
            fields.append(entry)
        changed = changed or tool_changed
        report_tools.append({"name": name, "status": "변경" if tool_changed else "일치", "fields": fields,
                             "sha_old": old["sha256"], "sha_new": new["sha256"]})

    for f in findings:
        print(f"의심 문구: {f['tool']} [{f['rule']}] {f['match']!r}")
    code = 1 if changed else (2 if findings else 0)
    if args.report:
        Path(args.report).parent.mkdir(parents=True, exist_ok=True)
        Path(args.report).write_text(json.dumps({
            "server": args.server, "checked_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "result": "불일치" if changed else "일치", "tools": report_tools, "findings": findings,
        }, indent=2, ensure_ascii=False), encoding="utf-8")
    if changed:
        print("결과: 불일치. 승인한 뒤 도구 정의가 바뀌었습니다.")
    elif findings:
        print("결과: 해시는 일치하지만 설명에 의심 문구가 있습니다.")
    else:
        print(f"결과: 일치. 도구 {len(current)}개가 고정한 값과 같습니다.")
    sys.exit(code)


if __name__ == "__main__":
    main()
