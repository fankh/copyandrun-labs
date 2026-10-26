#!/usr/bin/env bash
# 나이 정책 시험: 같은 의존성 범위에서 정책에 따라 어떤 cr-safe-util 버전이 고르는지 본다.
set -uo pipefail
DIR=${LAB:-$PWD}/age
rm -rf "$DIR"; mkdir -p "$DIR"; cd "$DIR"
printf 'registry=http://127.0.0.1:14873/\n' > .npmrc
echo '{ "name": "age-test", "version": "1.0.0", "private": true, "dependencies": { "cr-safe-util": "^1.0.0" } }' > package.json

picked() { node -p "require('./node_modules/cr-safe-util/package.json').version"; }

# 1.0.0 이 게시된 시각을 레지스트리에서 읽는다
T=$(curl -s http://127.0.0.1:14873/cr-safe-util | node -p "JSON.parse(require('fs').readFileSync(0,'utf8')).time['1.0.0']")
echo "1.0.0 게시 시각: $T"

rm -rf node_modules package-lock.json; npm install >/dev/null 2>&1
echo "정책 없음: $(picked)"

rm -rf node_modules package-lock.json; npm install --before="$T" >/dev/null 2>&1
echo "--before=1.0.0 게시 시각: $(picked)"

rm -rf node_modules package-lock.json
npm install --min-release-age=1 2>&1 | grep -E "npm error (code|notarget|No versions)" | head -2
