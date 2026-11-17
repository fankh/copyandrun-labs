#!/usr/bin/env bash
# MongoDB 를 인증 없음, 루트 하나로 공유, 최소 권한 세 상태로 띄우고 같은 다섯 가지 동작의 결과를 비교한다.
# 준비: Docker, 같은 폴더에 probe.js, plant.js, users.js. 내 컨테이너끼리만 접속한다(포트를 밖에 열지 않는다).
# 실행(Git Bash): bash mongo_demo.sh   (약 1분 30초). 종료 코드는 기대와 다른 칸의 수다(마지막 상태 기준).
export MSYS_NO_PATHCONV=1
HERE="$(pwd)"
IMG=mongo:8
ROOT='Root-lab-1'
cleanup() { docker rm -f osk-lb-db osk-lb-db2 >/dev/null 2>&1; docker network rm osk-lb-net >/dev/null 2>&1; }
cleanup; docker network create osk-lb-net >/dev/null
# M <호스트> <사용자:비밀번호 또는 빈 값> <스크립트>
M() {
  local uri="mongodb://$1/admin"
  [ -n "$2" ] && uri="mongodb://$2@$1/admin?authSource=admin"
  docker run --rm --network osk-lb-net -v "$HERE:/w:ro" $IMG mongosh --quiet "$uri" --file "/w/$3" 2>&1 | tail -1
}
wait_up() { for i in $(seq 1 40); do docker exec "$1" mongosh --quiet --eval 'db.runCommand({ping:1}).ok' 2>/dev/null | grep -q 1 && return; sleep 1; done; }
mismatch=0
check() {   # check <이름> <기대> <실제> : 칸별로 비교해 다른 칸 수를 센다
  local e=($2) a=($3) bad=0
  for i in 0 1 2 3 4; do [ "${e[$i]}" = "${a[$i]}" ] || bad=$((bad+1)); done
  printf "  %s | 기대 %s | 실제 %s | 다른 칸 %d\n" "$1" "$2" "$3" "$bad"
  mismatch=$((mismatch+bad))
}
echo "(열: shop 읽기, shop 쓰기, hr 읽기, 보이는 DB 수, DB 삭제)"

echo "## 1. 인증 없이 시작한 서버"
docker run -d --name osk-lb-db --network osk-lb-net $IMG >/dev/null; wait_up osk-lb-db
M osk-lb-db "" plant.js >/dev/null
check "익명" "X X X 0 X" "$(M osk-lb-db '' probe.js)"
echo -n "  다른 컨테이너가 shop.orders 지우기 전/후: "
docker run --rm --network osk-lb-net $IMG mongosh --quiet mongodb://osk-lb-db/shop --eval 'const b=db.orders.countDocuments({}); db.orders.drop(); print(b+" -> "+db.orders.countDocuments({}))' | tail -1
echo "  1단계 다른 칸 합계: $mismatch"
docker rm -f osk-lb-db >/dev/null

echo "## 2. 인증을 켰지만 앱이 루트 계정을 그대로 쓰는 서버"
mismatch=0
docker run -d --name osk-lb-db2 --network osk-lb-net -e MONGO_INITDB_ROOT_USERNAME=root -e MONGO_INITDB_ROOT_PASSWORD="$ROOT" $IMG >/dev/null
wait_up osk-lb-db2; sleep 6; wait_up osk-lb-db2
M osk-lb-db2 "root:$ROOT" plant.js >/dev/null
check "익명" "X X X 0 X" "$(M osk-lb-db2 '' probe.js)"
check "앱(root)" "O O X 1 X" "$(M osk-lb-db2 root:$ROOT probe.js)"
echo "  2단계 다른 칸 합계: $mismatch"

echo "## 3. 앱용과 보고용 사용자를 나눈 서버"
mismatch=0
M osk-lb-db2 "root:$ROOT" users.js >/dev/null
check "익명" "X X X 0 X" "$(M osk-lb-db2 '' probe.js)"
check "앱" "O O X 1 X" "$(M osk-lb-db2 app:App-lab-1 probe.js)"
check "보고" "X X O 1 X" "$(M osk-lb-db2 report:Report-lab-1 probe.js)"
check "관리자" "O O O 2 O" "$(M osk-lb-db2 root:$ROOT probe.js)"
echo "  3단계 다른 칸 합계: $mismatch"

echo "## 4. 교차 확인: connectionStatus 와 서버 로그"
for u in app:App-lab-1 report:Report-lab-1; do
  docker run --rm --network osk-lb-net $IMG mongosh --quiet "mongodb://$u@osk-lb-db2/admin?authSource=admin" --eval \
  'const s=db.runCommand({connectionStatus:1,showPrivileges:true}).authInfo; print(s.authenticatedUsers[0].user+" 역할 "+s.authenticatedUserRoles.map(r=>r.role+"@"+r.db)+" 권한 "+s.authenticatedUserPrivileges.length+"개, 대상 DB "+[...new Set(s.authenticatedUserPrivileges.map(p=>p.resource.db))])' | tail -1
done
echo -n "  틀린 비밀번호로 접속: "; docker run --rm --network osk-lb-net $IMG mongosh --quiet "mongodb://app:wrong@osk-lb-db2/admin?authSource=admin" --eval 'db.runCommand({ping:1})' 2>&1 | grep -o 'Authentication failed' | head -1
echo -n "  서버 로그의 'Failed to authenticate' 기록 수: "; docker logs osk-lb-db2 2>&1 | grep -c '"Failed to authenticate"'
echo -n "  그 기록의 사용자와 사유: "; docker logs osk-lb-db2 2>&1 | grep '"Failed to authenticate"' | grep -oE '"user":"[a-z]+"|"error":"[^"]*"' | tr '\n' ' '; echo
cleanup
echo "## 끝 (종료 코드 = 3단계 다른 칸 수)"
exit $mismatch
