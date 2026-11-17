#!/usr/bin/env python3
"""모드별 결과(TSV)를 요청 x 모드 표로 펼친다. 사용: python modsec_matrix.py ../osk-fc-ms-out"""
import glob
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
order = ["DetectionOnly-1", "On-1", "On-2", "On-3", "On-4"]
data = {}
for tag in order:
    for line in open(os.path.join(sys.argv[1], f"res-{tag}.tsv"), encoding="utf-8"):
        kind, name, code = line.rstrip("\n").split("\t")
        data.setdefault((kind, name), {})[tag] = code
print(f"{'요청':<16}" + "".join(f"{t:>16}" for t in order))
for (kind, name), row in data.items():
    print(f"{kind} {name:<14}" + "".join(f"{row[t]:>16}" for t in order))
