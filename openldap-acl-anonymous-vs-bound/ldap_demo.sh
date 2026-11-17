#!/usr/bin/env bash
# OpenLDAP(slapd) 컨테이너 두 개에 같은 사용자 항목을 넣고, ACL 이 느슨한 쪽과 좁힌 쪽을 익명, alice 로 나누어 점검한다.
# 준비: Docker, 같은 폴더에 slapd_bad.conf, slapd_good.conf, users.ldif. 비밀번호는 실행할 때마다 새로 정한다.
# 실행(Git Bash): bash ldap_demo.sh   (약 2분)
export MSYS_NO_PATHCONV=1
cleanup() { docker rm -f osk-fd-ldapbad osk-fd-ldapgood >/dev/null 2>&1; }
cleanup
BASE="dc=lab,dc=test"; ADMIN="cn=admin,$BASE"
ADMINPW=adminpw-$RANDOM; ALICEPW=alicepw-$RANDOM; BOBPW=bobpw-$RANDOM
start() {   # start <bad|good>
  local n=osk-fd-ldap$1
  docker run -d --name $n alpine sh -c 'apk add -q openldap openldap-back-mdb openldap-clients >/dev/null 2>&1; mkdir -p /var/lib/openldap/data; touch /ready; sleep 3600' >/dev/null
  until docker exec $n test -f /ready 2>/dev/null; do sleep 1; done
  local rp ap bp
  rp=$(docker exec $n slappasswd -s "$ADMINPW"); ap=$(docker exec $n slappasswd -s "$ALICEPW"); bp=$(docker exec $n slappasswd -s "$BOBPW")
  sed "s#@@ROOTPW@@#$rp#" slapd_$1.conf | docker exec -i $n sh -c 'cat > /etc/openldap/lab.conf'
  sed "s#@@ALICEPW@@#$ap#; s#@@BOBPW@@#$bp#" users.ldif | docker exec -i $n sh -c 'cat > /tmp/users.ldif'
  docker exec $n slapadd -f /etc/openldap/lab.conf -l /tmp/users.ldif >/dev/null 2>&1
  docker exec -d $n slapd -f /etc/openldap/lab.conf -h ldap://127.0.0.1:389 -d 0
  sleep 2
}
L() { local n=$1; shift; docker exec -i osk-fd-ldap$n "$@"; }   # L <bad|good> 명령... (표준 입력을 넘기려면 -i 가 필요하다)
SEARCH() { local n=$1; shift; L $n ldapsearch -x -LLL -H ldap://127.0.0.1 -b "$BASE" "$@" 2>&1; }
ALICE="uid=alice,ou=people,$BASE"; BOB="uid=bob,ou=people,$BASE"
MOD() {   # MOD <bad|good> <바꿀 항목 dn> <값> : alice 로 description 을 바꾸고 결과를 한 줄로 돌려준다
  local out
  out=$(printf 'dn: %s
changetype: modify
replace: description
description: %s
' "$2" "$3"     | L $1 sh -c "ldapmodify -x -H ldap://127.0.0.1 -D '$ALICE' -w '$ALICEPW'" 2>&1 | grep -v '^$' | tail -1)
  case "$out" in modifying*) echo "성공(변경됨)";; *) echo "$out";; esac
}
start bad; start good
violations=0
echo "## 1. 익명으로 검색"
for n in bad good; do
  out=$(SEARCH $n "(objectClass=inetOrgPerson)" uid userPassword mail)
  echo "  [$n] 보인 항목 $(echo "$out" | grep -c '^dn:')개, userPassword $(echo "$out" | grep -c '^userPassword'), mail $(echo "$out" | grep -c '^mail')"
done

echo "## 2. alice 로 로그인해 bob 의 정보를 읽고 고쳐 보기"
for n in bad good; do
  echo "  [$n]"
  out=$(SEARCH $n -D "$ALICE" -w "$ALICEPW" "(uid=bob)" userPassword mail)
  echo "    bob 의 userPassword 읽기: $(echo "$out" | grep -c '^userPassword')건, mail 읽기: $(echo "$out" | grep -c '^mail')건"
  echo "    bob 의 description 바꾸기: $(MOD $n "$BOB" hacked)"
  echo "    -> 다시 읽은 bob 의 description: $(SEARCH $n -D "$ALICE" -w "$ALICEPW" "(uid=bob)" description | grep '^description' | cut -c14-)"
  echo "    alice 본인의 description 바꾸기: $(MOD $n "$ALICE" mine)"
done

echo "## 3. slapacl 로 같은 질문을 설정 파일만으로 확인(서버를 거치지 않음)"
for n in bad good; do
  echo "  [$n]"
  for who in anonymous alice; do
    D=""; [ $who = alice ] && D="-D $ALICE"
    r=$(L $n slapacl -f /etc/openldap/lab.conf -b "$BOB" $D "userPassword/read" 2>&1 | tail -1)
    echo "    $who 가 bob 의 userPassword 읽기: ${r#*: }"
  done
done

echo "## 4. 게이트: 막혀야 하는 동작이 하나라도 허용되면 1"
for n in bad good; do
  v=0
  [ "$(SEARCH $n "(uid=bob)" userPassword | grep -c '^userPassword')" -gt 0 ] && v=$((v+1))                       # 익명이 비밀번호 해시를 읽음
  [ "$(SEARCH $n -D "$ALICE" -w "$ALICEPW" "(uid=bob)" userPassword | grep -c '^userPassword')" -gt 0 ] && v=$((v+1))   # 다른 사용자가 읽음
  case "$(MOD $n "$BOB" x)" in 성공*) v=$((v+1));; esac   # 다른 사용자가 고침
  echo "  $n: 허용되면 안 되는 동작 ${v}건 -> 종료 코드 $([ $v -gt 0 ] && echo 1 || echo 0)"
done
cleanup
echo "## 끝"
