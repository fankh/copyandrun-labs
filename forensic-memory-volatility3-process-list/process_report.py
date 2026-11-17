import json
import sys

# Volatility 3 의 pslist, psscan JSON 결과를 읽어 조사에 필요한 세 가지를 요약합니다.
#   1. 두 목록의 PID 집합 비교
#   2. ExitTime 이 있는 종료 프로세스
#   3. 부모가 목록에 없는 프로세스와, 알려진 부모 자식 관계에서 벗어난 프로세스
# 사용법: python3 process_report.py out/b_pslist.json out/b_psscan.json

# 윈도우 XP 기준으로 부모가 정해져 있는 시스템 프로세스 (이름은 15자에서 잘립니다)
EXPECTED_PARENT = {
    "smss.exe": "System",
    "csrss.exe": "smss.exe",
    "winlogon.exe": "smss.exe",
    "services.exe": "winlogon.exe",
    "lsass.exe": "winlogon.exe",
    "svchost.exe": "services.exe",
    "spoolsv.exe": "services.exe",
}
SINGLE = {"System", "smss.exe", "csrss.exe", "winlogon.exe", "services.exe", "lsass.exe"}


def load(path):
    with open(path, encoding="utf-8") as f:
        return {row["PID"]: row for row in json.load(f)}


def line(row):
    return f"PID {row['PID']:>5}  PPID {row['PPID']:>5}  {row['ImageFileName']}"


pslist = load(sys.argv[1])
psscan = load(sys.argv[2])

print("== 1. pslist 와 psscan 의 PID 집합 ==")
print(f"pslist {len(pslist)}개, psscan {len(psscan)}개")
only_scan = sorted(set(psscan) - set(pslist))
only_list = sorted(set(pslist) - set(psscan))
print(f"psscan 에만 있는 PID: {only_scan or '없음'}")
print(f"pslist 에만 있는 PID: {only_list or '없음'}")
for pid in only_scan:
    print("  확인 필요:", line(psscan[pid]), "종료 시각", psscan[pid]["ExitTime"])

print()
print("== 2. 종료된 프로세스 (ExitTime 이 있는 항목) ==")
rows = {**psscan, **pslist}
exited = [r for r in rows.values() if r["ExitTime"]]
for r in sorted(exited, key=lambda r: r["ExitTime"]):
    where = "pslist 에도 있음" if r["PID"] in pslist else "psscan 에만 있음"
    print(f"{line(r)}  시작 {r['CreateTime']}  종료 {r['ExitTime']}  ({where})")
if not exited:
    print("없음")

print()
print("== 3. 부모 자식 관계 점검 ==")
names = {pid: r["ImageFileName"] for pid, r in rows.items()}
orphans = [r for r in rows.values() if r["PPID"] not in rows and r["PPID"] != 0]
print("부모 PID 가 목록에 없는 프로세스 (부모가 이미 끝났거나 흔적이 지워졌을 수 있음):")
for r in sorted(orphans, key=lambda r: r["PID"]):
    print("  ", line(r))
if not orphans:
    print("   없음")
print("알려진 부모와 다른 프로세스:")
odd = 0
for r in sorted(rows.values(), key=lambda r: r["PID"]):
    want = EXPECTED_PARENT.get(r["ImageFileName"])
    got = names.get(r["PPID"])
    if want and got and got != want:
        odd += 1
        print("  ", line(r), f"-> 부모 {got}, 기대한 부모 {want}")
if not odd:
    print("   없음")
print("한 개만 있어야 하는 프로세스가 둘 이상인 경우:")
dup = 0
for name in sorted(SINGLE):
    alive = [r for r in rows.values() if r["ImageFileName"] == name and not r["ExitTime"]]
    if len(alive) > 1:
        dup += 1
        print("  ", name, [r["PID"] for r in alive])
if not dup:
    print("   없음")
