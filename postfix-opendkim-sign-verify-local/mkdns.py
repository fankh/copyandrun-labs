"""opendkim-genkey 가 만든 .txt 내용(표준 입력)을 dnsmasq 의 txt-record 한 줄로 바꿉니다."""
import re
import sys

text = sys.stdin.read()
name = text.split()[0] + ".example.internal"
parts = re.findall(r'"([^"]*)"', text)
value = "".join(parts)
chunks = [value[i:i + 200] for i in range(0, len(value), 200)]
print("txt-record=" + name + "," + ",".join('"' + c + '"' for c in chunks))
