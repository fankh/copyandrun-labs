#!/usr/bin/env bash
# PostgreSQL 역할 권한을 "느슨한 상태"와 "최소 권한 상태"로 나눠 같은 허용/거부 표로 검사하고, 어긋난 칸 수를 종료 코드로 낸다.
# 준비: Docker (postgres:16 이미지). 시험용 컨테이너라 비밀번호는 모두 lab 이다.
# 실행(Git Bash): bash roles_demo.sh   (약 40초)
export MSYS_NO_PATHCONV=1
N=osk-fb-pgr
docker rm -f $N >/dev/null 2>&1
docker run -d --name $N -e POSTGRES_PASSWORD=lab postgres:16 >/dev/null
for i in $(seq 1 30); do docker exec $N pg_isready -U postgres >/dev/null 2>&1 && break; sleep 1; done
sleep 2
SU() { docker exec -i $N psql -U postgres -d lab -At "$@" 2>&1; }
AS() { local u=$1; shift; docker exec -i -e PGPASSWORD=lab $N psql -h 127.0.0.1 -U "$u" -d lab -At "$@" 2>&1; }
docker exec $N psql -U postgres -c 'CREATE DATABASE lab' >/dev/null

# 기대하는 표(최소 권한 기준): 역할 | 실행할 문장 | 기대값
MATRIX=(
  "app_rw|SELECT count(*) FROM orders|ALLOW"
  "app_rw|INSERT INTO orders(item) VALUES ('x')|ALLOW"
  "app_rw|DELETE FROM orders|DENY"
  "app_rw|DROP TABLE orders|DENY"
  "app_rw|CREATE TABLE evil(a int)|DENY"
  "app_ro|SELECT count(*) FROM orders|ALLOW"
  "app_ro|INSERT INTO orders(item) VALUES ('x')|DENY"
  "app_ro|UPDATE orders SET item='y'|DENY"
  "app_ro|SELECT count(*) FROM invoices|ALLOW"
  "app_rw|INSERT INTO invoices(amount) VALUES (1)|ALLOW"
  "intruder|SELECT count(*) FROM orders|DENY"
  "intruder|CREATE TABLE evil(a int)|DENY"
)
try() {   # try <역할> <문장> : 권한 문제(permission denied, must be owner, CONNECT)로 막히면 DENY, 아니면 ALLOW (문장은 되돌린다)
  local out; out=$(echo "BEGIN; $2; ROLLBACK;" | AS "$1")
  if echo "$out" | grep -qE 'permission denied|must be owner|CONNECT privilege'; then echo DENY; else echo ALLOW; fi
}
check_all() {
  local bad=0 row role sql want got
  SU -c "SET ROLE $OWNER; CREATE TABLE invoices (id serial PRIMARY KEY, amount int); " >/dev/null   # 설정 뒤에 새로 생긴 표
  for row in "${MATRIX[@]}"; do
    IFS='|' read -r role sql want <<<"$row"
    got=$(try "$role" "$sql")
    mark="  "; [ "$got" != "$want" ] && { mark="X "; bad=$((bad+1)); }
    printf "  %s%-8s %-45s 기대 %-5s 실제 %s\n" "$mark" "$role" "$sql" "$want" "$got"
  done
  SU -c "SET ROLE $OWNER; DROP TABLE invoices" >/dev/null
  echo "  어긋난 칸: $bad / ${#MATRIX[@]}"
  return $((bad>0))
}

echo "## 1. 느슨한 상태(앱 역할이 표 주인, 읽기 역할에 ALL, 스키마를 PUBLIC 에 열어 둠)"
SU <<'SQL' >/dev/null
CREATE ROLE app_rw LOGIN PASSWORD 'lab';
CREATE ROLE app_ro LOGIN PASSWORD 'lab';
CREATE ROLE intruder LOGIN PASSWORD 'lab';
GRANT ALL ON SCHEMA public TO PUBLIC;
SET ROLE app_rw;
CREATE TABLE orders (id serial PRIMARY KEY, item text);
INSERT INTO orders(item) VALUES ('a'),('b');
RESET ROLE;
GRANT ALL ON ALL TABLES IN SCHEMA public TO app_ro;
SQL
OWNER=app_rw
check_all; echo "  게이트 종료 코드 $?"

echo "## 2. 최소 권한으로 고치기"
SU <<'SQL' >/dev/null
CREATE ROLE app_owner NOLOGIN;
ALTER TABLE orders OWNER TO app_owner;
ALTER SEQUENCE orders_id_seq OWNER TO app_owner;
REVOKE ALL ON ALL TABLES IN SCHEMA public FROM app_ro, app_rw;
REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE CONNECT ON DATABASE lab FROM PUBLIC;
GRANT CONNECT ON DATABASE lab TO app_rw, app_ro;
GRANT USAGE ON SCHEMA public TO app_rw, app_ro;
GRANT SELECT ON orders TO app_ro;
GRANT SELECT, INSERT, UPDATE ON orders TO app_rw;
GRANT USAGE ON SEQUENCE orders_id_seq TO app_rw;
ALTER DEFAULT PRIVILEGES FOR ROLE app_owner IN SCHEMA public GRANT SELECT ON TABLES TO app_ro;
ALTER DEFAULT PRIVILEGES FOR ROLE app_owner IN SCHEMA public GRANT SELECT, INSERT, UPDATE ON TABLES TO app_rw;
ALTER DEFAULT PRIVILEGES FOR ROLE app_owner IN SCHEMA public GRANT USAGE ON SEQUENCES TO app_rw;
SQL
OWNER=app_owner
echo "## 3. 같은 표로 다시 검사"
check_all; echo "  게이트 종료 코드 $?"

echo "## 4. 교차 확인: 내장 함수 has_table_privilege 와 실제 실행 결과"
SU -c "SELECT r, p, has_table_privilege(r, 'orders', p) FROM (VALUES ('app_rw'),('app_ro')) a(r), (VALUES ('SELECT'),('INSERT'),('DELETE')) b(p) ORDER BY 1,2" | tr '|' ' ' | sed 's/^/  /'
echo "## 5. 표의 권한 목록(\dp orders)"
docker exec $N psql -U postgres -d lab -At -c '\dp orders' | sed 's/^/  /'
docker rm -f $N >/dev/null 2>&1
echo "## 끝"
