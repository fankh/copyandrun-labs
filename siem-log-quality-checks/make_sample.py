import sys
from datetime import datetime, timedelta, timezone

CLEAN = "clean" in sys.argv  # clean 을 주면 문제가 없는 로그를 만듭니다

base = datetime(2026, 10, 1, 9, 0, 0, tzinfo=timezone.utc)
lines = []
for host in ("web01", "web02"):
    for seq in range(1, 11):
        if not CLEAN and host == "web01" and seq in (4, 5):
            continue                      # 유실: 4, 5번이 도착하지 않음
        t = base + timedelta(seconds=seq)
        ingested = t + timedelta(seconds=1)
        if not CLEAN and host == "web02" and seq == 7:
            t = t - timedelta(seconds=40)  # 시계가 40초 느린 호스트의 이벤트
        line = f"{t:%Y-%m-%dT%H:%M:%SZ} {ingested:%Y-%m-%dT%H:%M:%SZ} {host} seq={seq} GET /index 200"
        lines.append(line)
        if not CLEAN and host == "web01" and seq == 8:
            lines.append(line)            # 중복: 같은 줄이 두 번
if not CLEAN:
    lines.append("garbled line without fields")  # 파싱 실패
name = "clean.log" if CLEAN else "sample.log"
open(name, "w", encoding="utf-8").write("\n".join(lines) + "\n")
print(len(lines), "lines written")
