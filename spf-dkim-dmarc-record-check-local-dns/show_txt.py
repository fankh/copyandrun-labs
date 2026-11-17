"""이름마다 TXT 기록을 조각(문자열) 단위로 출력합니다. 사용법: python3 show_txt.py 이름 [이름 ...]"""
import sys

import dns.resolver

resolver = dns.resolver.Resolver(configure=False)
resolver.nameservers = ["127.0.0.1"]
for name in sys.argv[1:]:
    for rdata in resolver.resolve(name, "TXT"):
        print(f"{name}  (조각 {len(rdata.strings)}개)")
        for s in rdata.strings:
            text = s.decode()
            shown = text if len(text) <= 70 else text[:60] + "..." + text[-6:]
            print(f"  [{len(text):3}자] {shown}")
