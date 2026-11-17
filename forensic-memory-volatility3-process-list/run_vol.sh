#!/bin/sh
# 이미지 하나에 Volatility 3 플러그인 네 개를 실행해 out/ 에 저장합니다.
# 사용법: sh run_vol.sh <이미지 파일> <접두어>
set -e
IMG=$1
TAG=$2
mkdir -p out
vol -q -f "$IMG" windows.info > "out/${TAG}_info.txt"
for p in pslist pstree psscan; do
  vol -q -f "$IMG" windows.$p > "out/${TAG}_$p.txt"
done
for p in pslist psscan; do
  vol -q -r json -f "$IMG" windows.$p > "out/${TAG}_$p.json"
done
wc -l out/${TAG}_*.txt
