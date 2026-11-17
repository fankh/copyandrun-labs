"""JPEG 본문 그림과 안에 들어 있는 썸네일의 색을 비교합니다. 파일은 바꾸지 않습니다.

사용법: python compare_thumb.py 파일.jpg
본문 그림을 고치거나 가려도 EXIF 썸네일이 남아 있으면 예전 그림이 그대로 보입니다.
이 시험 파일은 본문이 파란색, 썸네일이 주황색이라 색으로 구분됩니다.
"""
import io
import sys

import piexif
from PIL import Image

path = sys.argv[1]
main = Image.open(path).convert("RGB")
thumb_bytes = piexif.load(path)["thumbnail"]
print("본문 그림 아래쪽 색 :", main.getpixel((main.width // 2, main.height - 1)))
if thumb_bytes:
    t = Image.open(io.BytesIO(thumb_bytes)).convert("RGB")
    print("썸네일 아래쪽 색    :", t.getpixel((t.width // 2, t.height - 1)), f"({t.width}x{t.height})")
else:
    print("썸네일              : 없음")
