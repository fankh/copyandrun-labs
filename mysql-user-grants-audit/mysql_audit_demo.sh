#!/usr/bin/env bash
# MySQL 8.0 사용자와 권한을 점검 질의로 감사하고(느슨한 상태 → 고친 상태), 실제 접속 시험과 대조하고, 심각한 발견이 있으면 종료 코드 1을 낸다.
# 준비: Docker (mysql:8.0 이미지). 시험용 컨테이너라 비밀번호는 모두 lab 이고 포트는 바깥에 열지 않는다.
# 실행(Git Bash): bash mysql_audit_demo.sh   (약 1분)
export MSYS_NO_PATHCONV=1
N=osk-fb-mysql
docker rm -f $N >/dev/null 2>&1
docker run -d --name $N -e MYSQL_ROOT_PASSWORD=lab mysql:8.0 >/dev/null
for i in $(seq 1 90); do
  [ "$(docker logs $N 2>&1 | grep -c 'ready for connections.*port: 3306')" -ge 1 ] && break; sleep 2
done
sleep 2
ROOT() { docker exec -i $N mysql -uroot -plab -N -B "$@" 2>&1 | grep -v 'Using a password'; }
AS()   { local u=$1; shift; docker exec -i $N mysql -u"$u" -plab -N -B "$@" 2>&1 | grep -v 'Using a password'; }

# 감사: 발견 한 줄에 [심각도] 계정 : 이유. 심각도 HIGH 가 하나라도 있으면 종료 코드 1
audit() {
  local high=0 n
  while IFS=$'\t' read -r sev acct why; do
    [ -z "$sev" ] && continue
    printf "  [%s] %-16s %s\n" "$sev" "$acct" "$why"
    [ "$sev" = HIGH ] && high=$((high+1))
  done < <(ROOT -e "
    SELECT 'HIGH',  CONCAT(user,'@',host), '비밀번호가 비어 있음' FROM mysql.user
      WHERE authentication_string='' AND account_locked='N' AND user NOT IN ('mysql.sys','mysql.session','mysql.infoschema');
    SELECT 'HIGH',  CONCAT(user,'@',host), 'GRANT OPTION 전체 권한(*.*)' FROM mysql.user
      WHERE Grant_priv='Y' AND Super_priv='Y' AND user NOT IN ('root','mysql.sys','mysql.session','mysql.infoschema');
    SELECT 'HIGH',  CONCAT(user,'@',host), 'FILE 또는 SUPER 전역 권한' FROM mysql.user
      WHERE (File_priv='Y' OR Super_priv='Y') AND Grant_priv='N' AND user NOT IN ('root','mysql.sys','mysql.session','mysql.infoschema');
    SELECT 'MEDIUM',CONCAT(user,'@',host), '모든 호스트(%)에서 접속 가능' FROM mysql.user
      WHERE host='%' AND user NOT IN ('mysql.sys','mysql.session','mysql.infoschema');
    SELECT 'MEDIUM',CONCAT(grantee), CONCAT('전역(*.*) 권한 ', COUNT(*), '개') FROM information_schema.USER_PRIVILEGES
      WHERE grantee NOT LIKE '\'root\'%' AND grantee NOT LIKE '\'mysql.%' GROUP BY grantee HAVING COUNT(*) > 1;" | sort -k1,1 -s)
  echo "  HIGH 발견 $high건"
  return $((high>0))
}

# 접속 시험: 사용자 | 문장 | 기대값 (DML 은 되돌리고, DDL 로 만든 것은 끝에 지운다)
MATRIX=(
  "app|SELECT COUNT(*) FROM shop.orders|ALLOW"
  "app|INSERT INTO shop.orders(item) VALUES ('x')|ALLOW"
  "app|SELECT COUNT(*) FROM mysql.user|DENY"
  "app|CREATE DATABASE evil_db|DENY"
  "app|CREATE USER probe@localhost|DENY"
  "report|SELECT COUNT(*) FROM shop.orders|ALLOW"
  "report|INSERT INTO shop.orders(item) VALUES ('x')|DENY"
  "report|SELECT COUNT(*) FROM mysql.user|DENY"
)
check_all() {
  local bad=0 row u sql want got out mark
  for row in "${MATRIX[@]}"; do
    IFS='|' read -r u sql want <<<"$row"
    out=$(echo "START TRANSACTION; $sql; ROLLBACK;" | AS "$u")
    if echo "$out" | grep -qE 'ERROR (1044|1045|1142|1227|1370)|denied'; then got=DENY; else got=ALLOW; fi
    mark="  "; [ "$got" != "$want" ] && { mark="X "; bad=$((bad+1)); }
    printf "  %s%-7s %-48s 기대 %-5s 실제 %s\n" "$mark" "$u" "$sql" "$want" "$got"
  done
  ROOT -e "DROP DATABASE IF EXISTS evil_db; DROP USER IF EXISTS probe@localhost;" >/dev/null
  echo "  어긋난 칸: $bad / ${#MATRIX[@]}"
  return $((bad>0))
}

ROOT -e "
CREATE DATABASE shop; CREATE TABLE shop.orders (id INT AUTO_INCREMENT PRIMARY KEY, item VARCHAR(20));
INSERT INTO shop.orders(item) VALUES ('a'),('b');
CREATE USER 'app'@'%'    IDENTIFIED BY 'lab';  GRANT ALL PRIVILEGES ON *.* TO 'app'@'%' WITH GRANT OPTION;
CREATE USER 'report'@'%' IDENTIFIED BY 'lab';  GRANT SELECT, INSERT, UPDATE, DELETE ON *.* TO 'report'@'%';
CREATE USER 'etl'@'%'    IDENTIFIED BY '';     GRANT FILE, PROCESS ON *.* TO 'etl'@'%';
CREATE USER 'app'@'localhost' IDENTIFIED BY 'lab';  GRANT ALL PRIVILEGES ON *.* TO 'app'@'localhost' WITH GRANT OPTION;
CREATE USER 'report'@'localhost' IDENTIFIED BY 'lab';  GRANT SELECT, INSERT, UPDATE, DELETE ON *.* TO 'report'@'localhost';" >/dev/null

echo "## 1. 느슨한 상태 감사"
audit; echo "  감사 게이트 종료 코드 $?"
echo "## 2. 느슨한 상태 접속 시험"
check_all; echo "  접속 게이트 종료 코드 $?"

echo "## 3. 최소 권한으로 고치기"
ROOT -e "
DROP USER 'etl'@'%'; DROP USER 'app'@'%'; DROP USER 'report'@'%';
REVOKE ALL PRIVILEGES, GRANT OPTION FROM 'app'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON shop.* TO 'app'@'localhost';
REVOKE ALL PRIVILEGES, GRANT OPTION FROM 'report'@'localhost';
GRANT SELECT ON shop.* TO 'report'@'localhost';
DROP USER IF EXISTS 'root'@'%';" >/dev/null
echo "## 4. 고친 상태 감사와 접속 시험"
audit; echo "  감사 게이트 종료 코드 $?"
check_all; echo "  접속 게이트 종료 코드 $?"

echo "## 5. 교차 확인: SHOW GRANTS"
for u in app report; do ROOT -e "SHOW GRANTS FOR '$u'@'localhost'" | sed "s/^/  /; s/ TO \`$u\`@\`localhost\`//"; done
echo "  MySQL $(ROOT -e 'SELECT VERSION()')"
docker rm -f $N >/dev/null 2>&1
echo "## 끝"
