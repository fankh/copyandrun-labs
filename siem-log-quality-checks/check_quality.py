import re
import sys
from collections import defaultdict
from datetime import datetime

MAX_DELAY = 5  # 초. 이벤트 시각과 수집 시각의 허용 차이
PATTERN = re.compile(r"^(\S+) (\S+) (\S+) seq=(\d+) ")


def parse_time(text):
    return datetime.strptime(text, "%Y-%m-%dT%H:%M:%SZ")


def analyze(path):
    """로그 파일을 읽어 점검 결과를 사전으로 돌려줍니다."""
    r = {"total": 0, "parse_failed": [], "duplicates": [], "hosts": {},
         "delay_problems": [], "reversals": [], "bad_lines": {}, "lines": []}
    seen = {}
    by_host = defaultdict(list)
    for number, raw in enumerate(open(path, encoding="utf-8"), 1):
        line = raw.rstrip("\n")
        r["total"] += 1
        r["lines"].append(line)
        m = PATTERN.match(line)
        if not m:
            r["parse_failed"].append(number)
            r["bad_lines"][number] = "파싱 실패"
            continue
        event, ingested, host, seq = parse_time(m[1]), parse_time(m[2]), m[3], int(m[4])
        if line in seen:
            r["duplicates"].append((number, seen[line]))
            r["bad_lines"][number] = "중복"
            continue
        seen[line] = number
        by_host[host].append((seq, event, number))
        delay = (ingested - event).total_seconds()
        if delay < 0 or delay > MAX_DELAY:
            r["delay_problems"].append((host, seq, delay))
            r["bad_lines"][number] = "시간 이상"
    for host, items in sorted(by_host.items()):
        seqs = sorted(s for s, _, _ in items)
        missing = [n for n in range(seqs[0], seqs[-1] + 1) if n not in set(seqs)]
        r["hosts"][host] = {"count": len(seqs), "first": seqs[0], "last": seqs[-1], "missing": missing}
        for (s1, t1, _), (s2, t2, n2) in zip(items, items[1:]):
            if t2 < t1:
                r["reversals"].append((host, s1, s2, int((t1 - t2).total_seconds())))
                r["bad_lines"].setdefault(n2, "순서 역전")
    return r


if __name__ == "__main__":
    r = analyze(sys.argv[1])
    print(f"전체 {r['total']}줄, 파싱 실패 {len(r['parse_failed'])}줄 (줄 번호 {r['parse_failed']})")
    d = r["duplicates"]
    print(f"중복 {len(d)}건 (줄 {d[0][0]} 은 줄 {d[0][1]} 과 같음)" if d else "중복 0건")
    for host, h in r["hosts"].items():
        print(f"{host}: 받은 {h['count']}건, 번호 {h['first']}~{h['last']}, 유실 {h['missing']}")
    for host, seq, delay in r["delay_problems"]:
        print(f"시간 이상: {host} seq={seq} 수집 시각과 이벤트 시각 차이 {delay:+.0f}초")
    for host, s1, s2, sec in r["reversals"]:
        print(f"순서 역전: {host} seq={s1} 다음 seq={s2} 의 이벤트 시각이 {sec}초 더 이른 시각")
