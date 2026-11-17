#!/usr/bin/env python3
"""Lynis 의 lynis-report.dat 을 읽어 점수, 경고, 제안을 요약하고, 기준 미달이면 종료 코드 1 로 끝낸다.
사용: python lynis_summary.py after.dat [--min 65] [--max-warnings 0] [--ignore ID,ID] [--diff before.dat]
(--diff 의 파일은 비교 대상인 이전 결과이고, 앞의 파일과 비교해 사라진 제안과 새로 생긴 제안을 보여 준다)"""
import sys

sys.stdout.reconfigure(encoding="utf-8")


def load(path):
    d = {"index": 0, "tests": 0, "warn": [], "sugg": []}
    for line in open(path, encoding="utf-8"):
        line = line.rstrip("\n")
        if line.startswith("hardening_index="):
            d["index"] = int(line.split("=")[1])
        elif line.startswith("lynis_tests_done="):
            d["tests"] = int(line.split("=")[1])
        elif line.startswith("warning[]="):
            d["warn"].append(line.split("=", 1)[1].split("|")[0])
        elif line.startswith("suggestion[]="):
            d["sugg"].append(line.split("=", 1)[1].split("|")[0])
    return d


args = sys.argv[1:]
opt = lambda name, default: type(default)(args[args.index(name) + 1]) if name in args else default
minimum, max_warn = opt("--min", 65), opt("--max-warnings", 0)
ignore = args[args.index("--ignore") + 1].split(",") if "--ignore" in args else []
path = args[0]
d = load(path)
print(f"== {path}")
d["warn"] = [w for w in d["warn"] if w not in ignore]
print(f"  하드닝 점수 {d['index']}, 수행한 점검 {d['tests']}개, 경고 {len(d['warn'])}개(무시 {len(ignore)}종 제외), 제안 {len(d['sugg'])}개")
if "--diff" in args:
    other = load(args[args.index("--diff") + 1])
    gone = sorted(set(other["sugg"]) - set(d["sugg"]))
    new = sorted(set(d["sugg"]) - set(other["sugg"]))
    print(f"  사라진 제안 {len(gone)}개: " + " ".join(gone))
    print(f"  새로 생긴 제안 {len(new)}개: " + " ".join(new))
ok = d["index"] >= minimum and len(d["warn"]) <= max_warn
print(f"  기준 점수 {minimum} 이상, 경고 {max_warn}개 이하 -> {'통과' if ok else '미달'}")
sys.exit(0 if ok else 1)
