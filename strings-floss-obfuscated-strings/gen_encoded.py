"""demo.c 에 넣을 인코딩 문자열을 만든다. XOR 키 0x5A 와 base64 두 가지."""
import base64

KEY = 0x5A
xor_text = "http://xor.example.com/a"
b64_text = "http://b64.example.com/c"

enc = bytes(b ^ KEY for b in xor_text.encode("ascii"))
print("XOR 바이트열:")
print("{ " + ", ".join(f"0x{b:02x}" for b in enc) + " }")
print("base64 문자열:")
print(base64.b64encode(b64_text.encode("ascii")).decode("ascii"))
