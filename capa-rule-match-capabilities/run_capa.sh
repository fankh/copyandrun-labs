#!/bin/sh
# 시험 프로그램 세 개를 capa 로 분석하고 결과를 JSON 으로 저장한다.
# 경로는 컨테이너 안 기준이다: capa 는 /opt/capa/capa, 규칙은 /opt/capa-rules-10.0.0
set -e
mkdir -p json
for name in empty fileio sockdemo; do
  /opt/capa/capa -r /opt/capa-rules-10.0.0 -j out/$name.exe > json/$name.json
done
ls -l json
