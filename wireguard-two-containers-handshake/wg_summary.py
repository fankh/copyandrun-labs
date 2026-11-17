#!/usr/bin/env python3
"""`wg show wg0 dump` 출력을 표준 입력으로 받아 핸드셰이크와 전송량을 보여 주고,
핸드셰이크가 없거나 ping 이 실패하면 종료 코드 1 로 끝낸다.
사용: wg show wg0 dump | python wg_summary.py --ping 0|1   (개인 키가 든 첫 줄은 읽지 않고 버린다)"""
import sys
import time

sys.stdout.reconfigure(encoding="utf-8")
ping_ok = sys.argv[sys.argv.index("--ping") + 1] == "1" if "--ping" in sys.argv else False
lines = [l for l in sys.stdin.read().splitlines() if l.strip()][1:]   # 첫 줄은 인터페이스(개인 키 포함)
if not lines:
    print("  피어 없음")
    sys.exit(1)
shake_ok = False
for l in lines:
    pub, _psk, endpoint, allowed, shake, rx, tx, _ka = l.split("\t")
    age = int(time.time()) - int(shake) if int(shake) else None
    shake_ok = shake_ok or age is not None
    print(f"  피어 {pub[:8]}…  핸드셰이크 {'없음' if age is None else f'{age}초 전'}  받음 {rx}B  보냄 {tx}B  허용 주소 {allowed}")
print(f"  ping {'성공' if ping_ok else '실패'}")
sys.exit(0 if (shake_ok and ping_ok) else 1)
