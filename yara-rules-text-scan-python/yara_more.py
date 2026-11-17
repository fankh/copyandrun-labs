"""YARA 심화: 16진수 패턴, 정규식, nocase/wide, 개수와 위치 조건, private 규칙, 검사 속도.

준비: pip install yara-python
주의: 모든 검사 대상은 이 파일 안에서 만든 문자열이다. 실제 악성코드를 쓰지 않는다.
실행: python -X utf8 yara_more.py   (약 10초)
"""
import os
import time

import yara

RULES = r'''
rule hex_header {
    meta: purpose = "실행 파일 머리(MZ 와 PE 표시)를 16진수로 찾는다"
    strings:
        $mz = { 4D 5A [2-60] 50 45 00 00 }          // MZ, 임의 2~60바이트, PE\0\0
    condition: $mz at 0
}
rule regex_domain {
    strings:
        $d = /https?:\/\/[a-z0-9.\-]+\.(ru|cn)\/[a-z0-9\/_]*/ nocase
    condition: $d
}
rule wide_password {
    strings:
        $a = "password" ascii nocase
        $w = "password" wide nocase
    condition: any of them
}
rule repeated_and_position {
    strings:
        $x = "ERROR"
    condition: #x > 3 and @x[1] < 20 and filesize < 1KB
}
private rule is_text {
    condition: uint8(0) >= 0x20 and uint8(0) < 0x7f
}
rule text_with_secret : sensitive text {
    meta: severity = "high"
    strings: $k = "api_key="
    condition: is_text and $k
}
'''
rules = yara.compile(source=RULES)

SAMPLES = {
    "MZ 머리가 있는 가짜 파일": b"MZ" + b"\x90\x00\x03\x00" + b"\x00" * 20 + b"PE\x00\x00" + b"data",
    "MZ 만 있고 PE 없음": b"MZ" + b"\x90\x00" * 30,
    "악성 주소가 든 글": b"visit http://bad-site.example.ru/dl/run_me now",
    "정상 주소": b"visit http://good.example.com/about",
    "ASCII 비밀번호": b"the Password is hidden",
    "UTF-16 비밀번호": "password".encode("utf-16-le"),
    "ERROR 다섯 번(짧은 파일)": b"ERROR a ERROR b ERROR c ERROR d ERROR e",
    "ERROR 다섯 번(큰 파일)": b"ERROR a ERROR b ERROR c ERROR d ERROR e" + b" " * 2000,
    "키가 든 글": b"config api_key=ABC123 end",
    "키가 든 이진 파일": b"\x00\x01api_key=ABC123",
}
print("## 1. 규칙 여섯 개를 시료 열 개에 적용한 결과")
print(f"  {'시료':<26}맞은 규칙")
for name, data in SAMPLES.items():
    m = rules.match(data=data)
    print(f"  {name:<26}{[x.rule for x in m] or '-'}")

print("\n## 2. 맞은 규칙의 정보(태그, 메타, 문자열 위치)")
m = rules.match(data=SAMPLES["키가 든 글"])[0]
print(f"  규칙 {m.rule}, 태그 {m.tags}, 메타 {m.meta}")
for sm in m.strings:
    for inst in sm.instances:
        print(f"  문자열 {sm.identifier} 위치 {inst.offset} 내용 {inst.matched_data!r}")
w = rules.match(data=SAMPLES["UTF-16 비밀번호"])[0]
print(f"  wide 규칙의 문자열: {[(s.identifier, i.offset, i.matched_data) for s in w.strings for i in s.instances]}")

print("\n## 3. 검사 속도: 무작위 1MB 파일 200개(규칙 6개)")
blobs = [os.urandom(1_000_000) for _ in range(200)]
t = time.time()
hits = sum(len(rules.match(data=b)) for b in blobs)
dt = time.time() - t
print(f"  {dt:.2f}초 ({200 / dt:.0f}개/초, {200 / dt:.0f}MB/초), 맞은 규칙 {hits}건")
fast = sum(len(rules.match(data=b, fast=True)) for b in blobs[:10])
print(f"  (fast 모드도 맞은 규칙 {fast}건. 무작위 데이터에는 맞는 것이 없어야 한다)")
