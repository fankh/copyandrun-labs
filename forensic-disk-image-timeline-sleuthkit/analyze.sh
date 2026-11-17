#!/bin/sh
# 증거 원본은 해시만 확인하고, 작업은 사본(work.img)에서 합니다.
set -e
export TZ=UTC
sha256sum -c evidence.sha256
cp evidence.img work.img
chmod 644 work.img
fls -r -m / work.img > body.txt
mactime -b body.txt -d -y > timeline.csv
wc -l body.txt timeline.csv
