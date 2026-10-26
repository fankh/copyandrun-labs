#!/usr/bin/env bash
# 사용법: bash make_packages.sh 1.0.0   (두 패키지 게시)
#         bash make_packages.sh 1.1.0   (cr-safe-util 에 postinstall 이 새로 생긴 버전 게시)
set -euo pipefail
REG=http://127.0.0.1:14873
VER=${1:-1.0.0}
WORK=${LAB:-$PWD}/pkgs
mkdir -p "$WORK"

# 게시용 계정 만들기(로컬 레지스트리 전용, 토큰은 publish.npmrc 에만 둔다)
if [ ! -f "$WORK/publish.npmrc" ]; then
  TOKEN=$(curl -s -X PUT -H 'Content-Type: application/json' \
    -d '{"name":"labuser","password":"lab-pass-123456"}' \
    "$REG/-/user/org.couchdb.user:labuser" | python -c "import sys,json;print(json.load(sys.stdin)['token'])")
  printf '//127.0.0.1:14873/:_authToken=%s\n' "$TOKEN" > "$WORK/publish.npmrc"
fi

# 정상 패키지
mkdir -p "$WORK/cr-safe-util"
cat > "$WORK/cr-safe-util/package.json" <<JSON
{ "name": "cr-safe-util", "version": "$VER", "main": "index.js", "license": "MIT" }
JSON
cat > "$WORK/cr-safe-util/index.js" <<'JS'
module.exports = { add: (a, b) => a + b };
JS
printf '# cr-safe-util

실습용 정상 패키지입니다. add 함수 하나만 제공합니다.
' > "$WORK/cr-safe-util/README.md"

if [ "$VER" != "1.0.0" ]; then
  # 새 버전에서 설치 스크립트가 추가된 상황을 흉내 낸다. 하는 일은 고정 문자열 출력뿐이다.
  cat > "$WORK/cr-safe-util/package.json" <<JSON
{ "name": "cr-safe-util", "version": "$VER", "main": "index.js", "license": "MIT",
  "scripts": { "postinstall": "node postinstall.js" } }
JSON
  cat > "$WORK/cr-safe-util/postinstall.js" <<'JS'
console.log('cr-safe-util postinstall ran (fixed string only)');
JS
fi

# 설치 스크립트가 있는 패키지(무해): 고정 문자열만 출력하고 표시 파일을 남긴다
if [ "$VER" = "1.0.0" ]; then
  mkdir -p "$WORK/cr-hook-demo"
  cat > "$WORK/cr-hook-demo/package.json" <<'JSON'
{ "name": "cr-hook-demo", "version": "1.0.0", "main": "index.js", "license": "MIT",
  "scripts": { "postinstall": "node postinstall.js" } }
JSON
  cat > "$WORK/cr-hook-demo/index.js" <<'JS'
module.exports = { hello: () => 'hello from cr-hook-demo' };
JS
  printf '# cr-hook-demo

실습용 패키지입니다. 설치할 때 postinstall 스크립트가 고정 문자열만 출력합니다.
' > "$WORK/cr-hook-demo/README.md"
  cat > "$WORK/cr-hook-demo/postinstall.js" <<'JS'
const fs = require('fs');
const path = require('path');
console.log('postinstall ran: fixed-string-only');
fs.writeFileSync(path.join(__dirname, 'postinstall-marker.txt'), 'postinstall ran: fixed-string-only\n');
JS
fi

for p in cr-safe-util cr-hook-demo; do
  [ -f "$WORK/$p/package.json" ] || continue
  [ "$VER" != "1.0.0" ] && [ "$p" = cr-hook-demo ] && continue
  (cd "$WORK/$p" && npm publish --registry "$REG" --userconfig "$WORK/publish.npmrc" --loglevel=error >/dev/null && echo "게시 완료: $p $(node -p "require('./package.json').version")")
done
