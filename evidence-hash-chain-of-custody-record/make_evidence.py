# 시험용 증거 파일을 만듭니다. 고정 시드로 만든 임의 바이트 4096개이며 내용에 의미는 없습니다.
import random
from pathlib import Path

Path("evidence").mkdir(exist_ok=True)
Path("evidence/disk-image-01.bin").write_bytes(random.Random(7).randbytes(4096))
print("만든 파일: evidence/disk-image-01.bin (4096 바이트)")
