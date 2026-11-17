#!/usr/bin/env bash
# PostgreSQL 행 수준 보안(RLS)을 끈 상태, 켠 상태, 정책을 붙인 상태로 나눠 같은 질의의 결과를 비교하고 합격/불합격 판정을 종료 코드로 낸다.
# 준비: Docker (postgres:16 이미지). 시험용 컨테이너라 비밀번호는 모두 lab 이다.
# 실행(Git Bash): bash rls_demo.sh   (약 40초)
export MSYS_NO_PATHCONV=1
N=osk-fb-pg
docker rm -f $N >/dev/null 2>&1
docker run -d --name $N -e POSTGRES_PASSWORD=lab postgres:16 >/dev/null
for i in $(seq 1 30); do docker exec $N pg_isready -U postgres >/dev/null 2>&1 && break; sleep 1; done
sleep 2
SU() { docker exec -i $N psql -U postgres -d lab -v ON_ERROR_STOP=0 -At "$@" 2>&1; }
AS() { local u=$1; shift; docker exec -i -e PGPASSWORD=lab $N psql -h 127.0.0.1 -U "$u" -d lab -At "$@" 2>&1; }
docker exec $N psql -U postgres -c 'CREATE DATABASE lab' >/dev/null

SU <<'SQL' >/dev/null
CREATE ROLE app_owner LOGIN PASSWORD 'lab';
CREATE ROLE alice LOGIN PASSWORD 'lab';
CREATE ROLE bob   LOGIN PASSWORD 'lab';
GRANT CREATE ON SCHEMA public TO app_owner;
SET ROLE app_owner;
CREATE TABLE docs (id serial PRIMARY KEY, owner text NOT NULL, title text NOT NULL);
GRANT SELECT, INSERT, UPDATE, DELETE ON docs TO alice, bob;
GRANT USAGE ON SEQUENCE docs_id_seq TO alice, bob;
INSERT INTO docs(owner,title) VALUES ('alice','a-1'),('alice','a-2'),('bob','b-1'),('bob','b-2');
SQL

# 판정: alice 가 자기 행만 보고, 남의 행을 쓰지 못하는지. 합격이면 0, 아니면 1
gate() {
  local seen others w1 w2
  seen=$(AS alice -c "SELECT count(*) FROM docs")
  others=$(AS alice -c "SELECT count(*) FROM docs WHERE owner <> 'alice'")
  # 쓰기 시험은 트랜잭션 안에서 하고 되돌려 자료를 바꾸지 않는다
  w1=$(echo "BEGIN; INSERT INTO docs(owner,title) VALUES ('bob','forged'); ROLLBACK;" | AS alice | grep -c 'row-level security')
  w2=$(echo "BEGIN; UPDATE docs SET title='x' WHERE owner='bob'; ROLLBACK;" | AS alice | grep '^UPDATE')
  echo "  alice 가 보는 행 $seen, 그중 남의 행 $others, 남의 이름으로 INSERT 거절 $w1, 남의 행 UPDATE 결과 '$w2'"
  [ "$others" = 0 ] && [ "$w1" = 1 ] && [ "$w2" = "UPDATE 0" ]
}
show() { echo "  $1 $(AS "$1" -c "SELECT count(*) FROM docs")행: $(AS "$1" -c "SELECT string_agg(title, ',' ORDER BY id) FROM docs")"; }

echo "## 1. RLS 를 켜지 않은 표(문제 있는 상태)"
show alice; show bob
gate; echo "  게이트 종료 코드 $?"

echo "## 2. RLS 만 켜고 정책이 없을 때(기본 거부)"
SU -c "ALTER TABLE docs ENABLE ROW LEVEL SECURITY" >/dev/null
show alice; show app_owner
echo "  표 소유자와 슈퍼유저는 정책을 건너뜁니다: $(SU -c "SELECT relrowsecurity, relforcerowsecurity FROM pg_class WHERE relname='docs'")"

echo "## 3. 정책을 붙인 뒤"
SU <<'SQL' >/dev/null
CREATE POLICY own_rows ON docs FOR ALL TO alice, bob
  USING (owner = current_user) WITH CHECK (owner = current_user);
SQL
show alice; show bob
gate; echo "  게이트 종료 코드 $?"
echo "  표 소유자 app_owner: $(AS app_owner -c "SELECT count(*) FROM docs")행(정책이 소유자에게는 적용되지 않음)"

echo "## 4. FORCE ROW LEVEL SECURITY 로 소유자도 정책 아래로"
SU -c "ALTER TABLE docs FORCE ROW LEVEL SECURITY" >/dev/null
echo "  표 소유자 app_owner: $(AS app_owner -c "SELECT count(*) FROM docs")행, 슈퍼유저 postgres: $(SU -c "SELECT count(*) FROM docs")행"
echo "  pg_policies: $(SU -c "SELECT policyname, cmd, roles FROM pg_policies WHERE tablename='docs'")"
echo "## 5. 표 정의에서 정책 확인(\d+)"
docker exec $N psql -U postgres -d lab -c '\d+ docs' | sed -n '/Policies/,/^Access/p'
echo "  서버 버전: $(SU -c 'SHOW server_version')"
docker rm -f $N >/dev/null 2>&1
echo "## 끝"
