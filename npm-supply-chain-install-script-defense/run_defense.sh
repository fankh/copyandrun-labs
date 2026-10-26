#!/usr/bin/env bash
# 같은 잠금 파일로 세 가지 설치 방식을 비교하고 결과를 results.json 에 남긴다.
set -uo pipefail
APP=${LAB:-$PWD}/app
MARK=node_modules/cr-hook-demo/postinstall-marker.txt
cd "$APP"
check() { [ -f "$MARK" ] && echo "실행됨" || echo "실행 안 됨"; }

rm -rf node_modules; npm ci >/dev/null 2>&1
A=$(check)
rm -rf node_modules; npm ci --ignore-scripts >/dev/null 2>&1
B=$(check)
npm rebuild cr-hook-demo >/dev/null 2>&1
C=$(check)
printf '{"default":"%s","ignore_scripts":"%s","after_rebuild":"%s"}\n' "$A" "$B" "$C" > "$APP/../results.json"
cat "$APP/../results.json"
