"""실행 파일을 열지 않고 바이트만 읽어서 XOR 인코딩 문자열을 찾는다.
키를 0x01~0xFF 까지 모두 대 보고, 풀린 결과가 'http' 로 시작하면 보여 준다."""
import re
import sys

data = open(sys.argv[1], "rb").read()

for key in range(1, 256):
    # 'http' 를 이 키로 XOR 한 4바이트가 파일 안 어디에 있는지 찾는다
    needle = bytes(b ^ key for b in b"http")
    for m in re.finditer(re.escape(needle), data):
        chunk = data[m.start():m.start() + 40]
        text = bytes(b ^ key for b in chunk)
        end = text.find(b"\x00")
        text = text[:end] if end >= 0 else text
        # 읽을 수 있는 글자만 이어지는 앞부분까지 자른다
        ok = re.match(rb"[\x20-\x7e]+", text)
        if ok and len(ok.group()) >= 12 and key != 0:
            print(f"키 0x{key:02x}, 위치 0x{m.start():x}: {ok.group().decode()}")
