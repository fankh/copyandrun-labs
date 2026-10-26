#!/bin/bash
# 스킬을 다시 쓸 때 결과가 달라지도록 로그에 ERROR 줄 3개를 더합니다. 컨테이너 안에서만 실행합니다.
for t in 09:10:00 09:11:00 09:12:00; do
  echo "2026-10-24 $t ERROR disk full" >> "$HOME/practice/app.log"
done
wc -l "$HOME/practice/app.log"
