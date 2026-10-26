#!/usr/bin/env bash
# 두 패키지를 쓰는 샘플 앱을 만든다. 레지스트리는 로컬 Verdaccio 로 고정한다.
set -euo pipefail
APP=${LAB:-$PWD}/app
mkdir -p "$APP"
cat > "$APP/package.json" <<'JSON'
{
  "name": "sample-app",
  "version": "1.0.0",
  "private": true,
  "dependencies": {
    "cr-safe-util": "^1.0.0",
    "cr-hook-demo": "1.0.0"
  }
}
JSON
cat > "$APP/app.js" <<'JS'
const util = require('cr-safe-util');
const demo = require('cr-hook-demo');
console.log('2 + 3 =', util.add(2, 3), '/', demo.hello());
JS
printf 'registry=http://127.0.0.1:14873/\n' > "$APP/.npmrc"
