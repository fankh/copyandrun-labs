"""오탐 확인용 파일 네 개를 samples/ 에 만듭니다(모두 무해한 자료, 표준 라이브러리만 사용).

notes.txt   평범한 영문 텍스트
archive.zip 위 텍스트와 비슷한 글 여러 개를 zip 으로 압축한 것
image.png   무작위 픽셀로 채운 PNG 이미지
secret.bin  무작위 바이트(암호화된 자료처럼 보이는 것)
"""
import os
import random
import struct
import zipfile
import zlib
from pathlib import Path

out = Path("samples")
out.mkdir(exist_ok=True)
rnd = random.Random(1)

words = "alpha bravo charlie delta echo foxtrot golf hotel india juliet kilo lima".split()
text = "\n".join(" ".join(rnd.choice(words) for _ in range(12)) for _ in range(800))
(out / "notes.txt").write_text(text, encoding="utf-8")

with zipfile.ZipFile(out / "archive.zip", "w", zipfile.ZIP_DEFLATED) as z:
    for i in range(5):
        z.writestr(f"part{i}.txt", text)


def chunk(tag: bytes, body: bytes) -> bytes:
    return struct.pack(">I", len(body)) + tag + body + struct.pack(">I", zlib.crc32(tag + body))


w = h = 120
rows = b"".join(b"\x00" + bytes(rnd.randrange(256) for _ in range(w * 3)) for _ in range(h))
png = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
png += chunk(b"IDAT", zlib.compress(rows)) + chunk(b"IEND", b"")
(out / "image.png").write_bytes(png)

(out / "secret.bin").write_bytes(os.urandom(20000))
print("만든 파일:", ", ".join(sorted(p.name for p in out.iterdir())))
