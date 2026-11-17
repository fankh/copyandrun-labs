#!/bin/sh
# 자기 소유 연습 대역(192.168.88.10-40)만 점검합니다. 사용법: sh scan.sh before   (결과: scan-before.xml, scan-before.gnmap)
LABEL=${1:-before}
TARGET=192.168.88.10-40
docker rm -f cr-p24-scan >/dev/null 2>&1
docker run --name cr-p24-scan --network cr-p24-net --ip 192.168.88.50 instrumentisto/nmap \
  -sT -sV -n -oX - -oG /tmp/g.gnmap $TARGET > "scan-$LABEL.xml"
docker cp cr-p24-scan:/tmp/g.gnmap "scan-$LABEL.gnmap"
docker rm -f cr-p24-scan >/dev/null
echo "저장: scan-$LABEL.xml, scan-$LABEL.gnmap"
