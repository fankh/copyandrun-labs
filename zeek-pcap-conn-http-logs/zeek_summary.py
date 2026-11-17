#!/usr/bin/env python3
"""Zeek 의 JSON 로그(conn.log, http.log)를 요약하고, 한 출발지의 404 응답이 기준을 넘으면 종료 코드 1 로 끝낸다.
사용: python zeek_summary.py 로그폴더 [--max404 5] [--pcap-packets N]"""
import collections
import json
import sys

sys.stdout.reconfigure(encoding="utf-8")


def rows(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


args = sys.argv[1:]
folder = args[0]
limit = int(args[args.index("--max404") + 1]) if "--max404" in args else 5
pcap_packets = int(args[args.index("--pcap-packets") + 1]) if "--pcap-packets" in args else None

conn = rows(f"{folder}/conn.json")
http = rows(f"{folder}/http.json")
tcp = [c for c in conn if c.get("proto") == "tcp"]
pkts = sum(c.get("orig_pkts", 0) + c.get("resp_pkts", 0) for c in tcp)
print(f"  연결 {len(conn)}개(TCP {len(tcp)}개, 그 밖 {len(conn) - len(tcp)}개), TCP 패킷 합계 {pkts}개, HTTP 요청 {len(http)}건")
if pcap_packets is not None:
    print(f"  pcap 의 TCP 패킷 수 {pcap_packets}개 -> {'일치' if pcap_packets == pkts else '불일치'}")
codes = collections.Counter(h.get("status_code") for h in http)
print("  응답 코드: " + ", ".join(f"{k} x{v}" for k, v in sorted(codes.items(), key=lambda x: str(x[0]))))
agents = collections.Counter(h.get("user_agent", "-") for h in http)
print("  User-Agent: " + ", ".join(f"{k} x{v}" for k, v in agents.items()))
n404 = collections.Counter(h["id.orig_h"] for h in http if h.get("status_code") == 404)
worst = max(n404.values(), default=0)
print(f"  한 출발지의 404 최대 {worst}건 (허용 {limit}건)")
sys.exit(1 if worst > limit else 0)
