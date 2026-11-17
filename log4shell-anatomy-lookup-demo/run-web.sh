#!/bin/sh
# 사용: sh run-web.sh <log4j 버전> [자바 옵션]
# 1단계: 라이브러리를 내려받아 빌드한다 (이때만 네트워크 사용)
# 2단계: 컨테이너를 127.0.0.1:18080 에만 열어 실행한다. 확인이 끝나면 docker rm -f l4s-web
set -e
V="$1"; OPT="$2"
IMG=maven:3.9-eclipse-temurin-21

docker rm -f l4s-web >/dev/null 2>&1 || true

docker run --rm -v "$(pwd)":/w -v l4s-m2:/m2 -w /w $IMG \
  sh -c "rm -rf target && mvn -q -Dlog4j.version=$V -Dmaven.repo.local=/m2 package dependency:copy-dependencies -DoutputDirectory=target/dep >/dev/null 2>&1"

docker run -d --name l4s-web -p 127.0.0.1:18080:8080 -v "$(pwd)":/w -w /w $IMG \
  sh -c "java $OPT -cp 'target/classes:target/dep/*' WebApp"
echo "http://127.0.0.1:18080 에서 확인합니다."
