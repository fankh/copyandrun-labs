"""auth.log 에서 SSH 침입 흔적을 시간순으로 읽는 분석 스크립트입니다.

사용법: python3 triage.py /var/log/auth.log [--threshold 3]
1) IP별 실패 횟수  2) 실패 뒤 첫 성공 로그인  3) 성공한 세션 안의 sudo 와 계정 생성 기록
"""
import re
import sys
from collections import defaultdict
from datetime import datetime

LINE = re.compile(r"^(\S+) (\S+) ([\w.-]+)(?:\[(\d+)\])?: (.*)$")
FAILED = re.compile(r"Failed password for (?:invalid user )?(\S+) from (\S+) port \d+")
ACCEPT = re.compile(r"Accepted (\w+) for (\S+) from (\S+) port \d+")
CLOSED = re.compile(r"session closed for user (\S+)")
SUDO = re.compile(r"^\s*(\S+) : .*?USER=(\S+) ; COMMAND=(.*)$")
NEWUSER = re.compile(r"new user: name=([^,]+)")


def parse(path):
    fails = defaultdict(list)      # IP -> [(시각, 계정)]
    sessions = {}                  # sshd PID -> 세션 정보
    sudos, adds = [], []
    with open(path, encoding="utf-8", errors="replace") as f:
        for raw in f:
            m = LINE.match(raw.rstrip("\n"))
            if not m:
                continue
            ts = datetime.fromisoformat(m.group(1))
            proc, pid, msg = m.group(3), m.group(4), m.group(5)
            if proc == "sshd":
                if (x := FAILED.search(msg)):
                    fails[x.group(2)].append((ts, x.group(1)))
                elif (x := ACCEPT.search(msg)):
                    sessions[pid] = {"start": ts, "end": None, "method": x.group(1),
                                     "user": x.group(2), "ip": x.group(3)}
                elif (x := CLOSED.search(msg)) and pid in sessions:
                    sessions[pid]["end"] = ts
            elif proc == "sudo" and (x := SUDO.match(msg)):
                sudos.append((ts, x.group(1), x.group(2), x.group(3)))
            elif proc == "useradd" and (x := NEWUSER.search(msg)):
                adds.append((ts, x.group(1)))
    return fails, sessions, sudos, adds


def hms(ts):
    return ts.strftime("%H:%M:%S")


def main():
    path = sys.argv[1]
    threshold = int(sys.argv[sys.argv.index("--threshold") + 1]) if "--threshold" in sys.argv else 3
    fails, sessions, sudos, adds = parse(path)

    print("[1] IP별 실패 횟수")
    print(f"{'IP':<14}{'실패':>4}  {'시도한 계정':<22}첫 시각 ~ 마지막 시각")
    for ip, items in sorted(fails.items(), key=lambda kv: -len(kv[1])):
        users = sorted({u for _, u in items})
        print(f"{ip:<14}{len(items):>4}  {','.join(users):<22}{hms(items[0][0])} ~ {hms(items[-1][0])}")

    print(f"\n[2] 실패 뒤 첫 성공 로그인 (기준: 실패 {threshold}회 이상)")
    hits, last_ok = [], {}
    for pid, s in sorted(sessions.items(), key=lambda kv: kv[1]["start"]):
        floor = last_ok.get(s["ip"], datetime.min.replace(tzinfo=s["start"].tzinfo))
        before = [t for t, _ in fails.get(s["ip"], []) if floor < t < s["start"]]
        last_ok[s["ip"]] = s["start"]
        flag = "의심" if len(before) >= threshold else "참고"
        print(f"{flag}  {hms(s['start'])}  {s['user']} 출처 {s['ip']}  {s['method']}  직전 실패 {len(before)}회")
        if flag == "의심":
            hits.append((pid, s, floor))

    print("\n[3] 의심 세션의 시간순 타임라인")
    for pid, s, floor in hits:
        end = s["end"] or datetime.max.replace(tzinfo=s["start"].tzinfo)
        events = [(t, f"실패 {u}") for t, u in fails[s["ip"]] if floor < t < s["start"]]
        events.append((s["start"], f"성공 로그인 {s['user']} ({s['method']})"))
        events += [(t, f"sudo {tgt}: {cmd}") for t, who, tgt, cmd in sudos
                   if who == s["user"] and s["start"] <= t <= end]
        events += [(t, f"계정 생성 {name}") for t, name in adds if s["start"] <= t <= end]
        if s["end"]:
            events.append((s["end"], "세션 종료"))
        print(f"세션 sshd[{pid}] 출처 {s['ip']}")
        for t, text in sorted(events):
            print(f"  {hms(t)}  {text}")


if __name__ == "__main__":
    main()
