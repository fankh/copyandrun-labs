#!/bin/sh
# 컨테이너 안에서 컴파일러와 capa, 규칙을 준비한다.
# 컨테이너는 python:3.12-slim 에서 시작했다(root 로 실행).
set -e
apt-get update -qq
apt-get install -y -qq mingw-w64 curl unzip binutils-mingw-w64-x86-64 > /dev/null
cd /tmp
curl -sL -o capa.zip https://github.com/mandiant/capa/releases/download/v10.0.0/capa-v10.0.0-linux.zip
curl -sL -o rules.zip https://github.com/mandiant/capa-rules/archive/refs/tags/v10.0.0.zip
mkdir -p /opt/capa
unzip -q -o capa.zip -d /opt/capa
unzip -q -o rules.zip -d /opt
chmod +x /opt/capa/capa
/opt/capa/capa --version
x86_64-w64-mingw32-gcc --version | head -1
