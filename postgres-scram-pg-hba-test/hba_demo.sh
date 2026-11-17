#!/usr/bin/env bash
# PostgreSQL 의 pg_hba.conf 를 "trust 로 전부 열림", "규칙만 고침(비밀번호는 md5 그대로)", "규칙과 SCRAM 모두 고침" 세 단계로 바꿔 가며
# 서로 다른 두 클라이언트 컨테이너에서 같은 6가지 접속을 시도하고, 기대와 어긋난 개수를 종료 코드로 낸다.
# 준비: Docker (postgres:16 이미지), 같은 폴더에 pg_hba_bad.conf, pg_hba_good.conf. 시험용이라 비밀번호는 lab-pw 이다.
# 실행(Git Bash): bash hba_demo.sh   (약 1분)
export MSYS_NO_PATHCONV=1
HERE="$(pwd)"
NET=osk-l1b-net; DB=osk-l1b-db; APP=osk-l1b-app; OTH=osk-l1b-other
cleanup() { docker rm -f $DB $APP $OTH >/dev/null 2>&1; docker network rm $NET >/dev/null 2>&1; }
cleanup
docker network create --subnet 10.231.77.0/24 $NET >/dev/null
docker run -d --name $DB  --network $NET --ip 10.231.77.2  -e POSTGRES_PASSWORD=admin-pw postgres:16 >/dev/null
docker run -d --name $APP --network $NET --ip 10.231.77.10 postgres:16 sleep infinity >/dev/null
docker run -d --name $OTH --network $NET --ip 10.231.77.20 postgres:16 sleep infinity >/dev/null
for i in $(seq 1 40); do docker exec $DB pg_isready -U postgres >/dev/null 2>&1 && break; sleep 1; done; sleep 3

SU() { docker exec -i $DB psql -U postgres -At "$@" 2>&1; }   # 컨테이너 안의 소켓(local trust)으로 관리 작업
SU -c "ALTER SYSTEM SET password_encryption='md5'" >/dev/null     # 처음엔 일부러 옛 방식(md5)으로 저장
SU -c "SELECT pg_reload_conf()" >/dev/null
SU -c "CREATE DATABASE lab" >/dev/null
SU -c "CREATE ROLE app LOGIN PASSWORD 'lab-pw'" >/dev/null
use_hba() { docker exec -i $DB sh -c 'cat > "$PGDATA/pg_hba.conf"' < "$HERE/$1"; SU -c "SELECT pg_reload_conf()" >/dev/null; sleep 1; }

# 접속 시도: try <클라이언트 컨테이너> <사용자> <비밀번호|-> <데이터베이스> → ALLOW 또는 DENY(이유)
try() {
  local c=$1 u=$2 p=$3 d=$4 out
  if [ "$p" = "-" ]; then p=""; fi
  out=$(docker exec -e PGPASSWORD="$p" -e PGCONNECT_TIMEOUT=5 $c psql "host=10.231.77.2 user=$u dbname=$d" -w -At -c "select 1" 2>&1)
  if [ "$out" = "1" ]; then echo "ALLOW"; else echo "DENY|$(echo "$out" | head -1 | sed -E 's/^.*FATAL:  //; s/, no encryption//; s/pg_hba.conf rejects connection for host/pg_hba 거절: host/' | cut -c1-100)"; fi
}
# 기대하는 표: 이름 | 클라이언트 | 사용자 | 비밀번호 | 데이터베이스 | 기대
MATRIX=(
  "1 app 서버에서 app, 맞는 비밀번호|$APP|app|lab-pw|lab|ALLOW"
  "2 app 서버에서 app, 틀린 비밀번호|$APP|app|wrong|lab|DENY"
  "3 app 서버에서 postgres, 비밀번호 없이|$APP|postgres|-|lab|DENY"
  "4 다른 서버에서 app, 맞는 비밀번호|$OTH|app|lab-pw|lab|DENY"
  "5 다른 서버에서 postgres, 비밀번호 없이|$OTH|postgres|-|lab|DENY"
  "6 app 서버에서 app, postgres DB|$APP|app|lab-pw|postgres|DENY"
)
run_matrix() {
  local bad=0 row name c u p d want got
  for row in "${MATRIX[@]}"; do
    IFS='|' read -r name c u p d want <<<"$row"
    got=$(try $c $u $p $d)
    if [ "${got%%|*}" = "$want" ]; then mark="맞음"; else mark="어긋남"; bad=$((bad+1)); fi
    printf "  %s 기대 %-5s 실제 %-5s %s
" "$mark" "$want" "${got%%|*}" "${name#* }"
    [ "$got" != "${got%%|*}" ] && echo "           - ${got#*|}"
  done
  echo "  어긋난 칸: $bad / ${#MATRIX[@]}"
  return $bad
}
hash_kind() { SU -c "SELECT rolname || ' ' || left(rolpassword, 14) FROM pg_authid WHERE rolname='app'"; }

echo "## 1. 느슨한 상태: host all all 0.0.0.0/0 trust, 비밀번호는 md5 저장"
use_hba pg_hba_bad.conf
echo "  저장된 해시: $(hash_kind)"
run_matrix; R1=$?

echo "## 2. 규칙만 고침: pg_hba 는 scram-sha-256 인데 app 의 비밀번호는 md5 로 저장된 채"
use_hba pg_hba_good.conf
run_matrix; R2=$?
echo "  서버 로그: $(docker logs $DB 2>&1 | grep -m1 'valid SCRAM secret' | sed -E 's/^.*DETAIL:  /DETAIL: /')"

echo "## 3. 저장 방식도 고침: password_encryption 을 scram 으로 바꾸고 비밀번호를 다시 설정"
SU -c "ALTER SYSTEM SET password_encryption='scram-sha-256'" >/dev/null; SU -c "SELECT pg_reload_conf()" >/dev/null
SU -c "ALTER ROLE app PASSWORD 'lab-pw'" >/dev/null
echo "  저장된 해시: $(hash_kind)"
run_matrix; R3=$?

echo "## 4. pg_hba_file_rules 로 규칙 교차 확인(error 열이 비어 있어야 함)"
SU -c "SELECT line_number, type, database, user_name, address, auth_method, coalesce(error,'-') FROM pg_hba_file_rules" | sed 's/^/  /'
cleanup
echo "## 요약: 1단계 어긋남 $R1, 2단계 어긋남 $R2, 3단계 어긋남 $R3"
[ $R3 -eq 0 ] && echo "  게이트: 최종 상태 통과(종료 코드 0)" || echo "  게이트: 실패"
exit $R3
