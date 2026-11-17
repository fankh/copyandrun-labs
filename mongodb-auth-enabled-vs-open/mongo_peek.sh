#!/usr/bin/env bash
# 같은 공격자 시점 스크립트(peek.js)를 인증 없는 서버, 앱 계정, 인증 없이 인증 켠 서버에 돌려 보이는 것과 오류 문구를 비교한다.
# 준비: Docker, 같은 폴더에 peek.js, plant.js, users.js. 실행(Git Bash): bash mongo_peek.sh   (약 1분)
export MSYS_NO_PATHCONV=1
HERE="$(pwd)"; IMG=mongo:8; ROOT='Root-lab-1'
cleanup() { docker rm -f osk-lb-db osk-lb-db2 >/dev/null 2>&1; docker network rm osk-lb-net >/dev/null 2>&1; }
cleanup; docker network create osk-lb-net >/dev/null
M() { local uri="mongodb://$1/admin"; [ -n "$2" ] && uri="mongodb://$2@$1/admin?authSource=admin"
  docker run --rm --network osk-lb-net -v "$HERE:/w:ro" $IMG mongosh --quiet "$uri" --file "/w/$3" 2>&1; }
wait_up() { for i in $(seq 1 40); do docker exec "$1" mongosh --quiet --eval 'db.runCommand({ping:1}).ok' 2>/dev/null | grep -q 1 && return; sleep 1; done; }
echo "## 인증 없는 서버, 로그인 없이"
docker run -d --name osk-lb-db --network osk-lb-net $IMG >/dev/null; wait_up osk-lb-db
M osk-lb-db "" plant.js >/dev/null; M osk-lb-db "" peek.js
docker rm -f osk-lb-db >/dev/null
docker run -d --name osk-lb-db2 --network osk-lb-net -e MONGO_INITDB_ROOT_USERNAME=root -e MONGO_INITDB_ROOT_PASSWORD="$ROOT" $IMG >/dev/null
wait_up osk-lb-db2; sleep 6; wait_up osk-lb-db2
M osk-lb-db2 "root:$ROOT" plant.js >/dev/null; M osk-lb-db2 "root:$ROOT" users.js >/dev/null
echo "## 인증을 켠 서버, 로그인 없이"; M osk-lb-db2 "" peek.js
echo "## 인증을 켠 서버, 앱 계정(shop 읽기쓰기)으로"; M osk-lb-db2 "app:App-lab-1" peek.js
cleanup
