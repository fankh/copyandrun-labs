#!/usr/bin/env bash
# Redis ACL 을 "느슨한 상태"와 "최소 권한 상태"로 나눠 같은 허용/거부 표로 검사하고, ACL DRYRUN 과 ACL LOG 로 교차 확인한다.
# 준비: Docker (redis:7-alpine). 시험용 컨테이너라 비밀번호는 모두 lab 이고 포트는 바깥에 열지 않는다.
# 실행(Git Bash): bash redis_acl_demo.sh   (약 15초)
export MSYS_NO_PATHCONV=1
N=osk-fb-redis
docker rm -f $N >/dev/null 2>&1
docker run -d --name $N redis:7-alpine >/dev/null
sleep 2
R()  { docker exec $N redis-cli --no-auth-warning "$@" 2>&1; }             # 인증 없이(default 사용자)
RU() { local u=$1; shift; docker exec $N redis-cli --no-auth-warning --user "$u" --pass lab "$@" 2>&1; }
AD() { RU admin "$@"; }                                                     # 설정과 점검에만 쓰는 관리자(default 를 끄기 전에 만들어 둔다)
R ACL SETUSER admin on '>lab' '~*' '&*' '+@all' >/dev/null

# 기대하는 표(최소 권한 기준): 사용자 | 명령 | 기대값
MATRIX=(
  "anon|GET app:1|DENY"
  "app|SET app:1 hello|ALLOW"
  "app|GET app:1|ALLOW"
  "app|GET other:1|DENY"
  "app|KEYS *|DENY"
  "app|CONFIG GET dir|DENY"
  "app|FLUSHALL|DENY"
  "reader|GET app:1|ALLOW"
  "reader|SET app:1 x|DENY"
)
try() {   # try <사용자> <명령...> : NOPERM, NOAUTH, WRONGPASS 가 나오면 DENY
  local u=$1; shift; local out
  if [ "$u" = anon ]; then out=$(R "$@"); else out=$(RU "$u" "$@"); fi
  if echo "$out" | grep -qE 'NOPERM|NOAUTH|WRONGPASS'; then echo DENY; else echo ALLOW; fi
}
check_all() {
  local bad=0 row u cmd want got mark
  AD SET app:1 seed >/dev/null; AD SET other:1 seed >/dev/null            # 시험 전에 자료를 채움
  for row in "${MATRIX[@]}"; do
    IFS='|' read -r u cmd want <<<"$row"
    got=$(try "$u" $cmd)
    mark="  "; [ "$got" != "$want" ] && { mark="X "; bad=$((bad+1)); }
    printf "  %s%-7s %-22s 기대 %-5s 실제 %s\n" "$mark" "$u" "$cmd" "$want" "$got"
  done
  echo "  어긋난 칸: $bad / ${#MATRIX[@]}"
  return $((bad>0))
}

echo "## 1. 느슨한 상태(default 사용자는 비밀번호 없음, 앱과 읽기 사용자도 모든 명령과 키 허용)"
AD ACL SETUSER app on '>lab' '~*' '&*' '+@all' >/dev/null
AD ACL SETUSER reader on '>lab' '~*' '&*' '+@all' >/dev/null
echo "  default 사용자 규칙: $(AD ACL LIST | grep '^user default' | sed 's/sanitize-payload //')"
echo "  app 사용자 규칙:     $(AD ACL LIST | grep '^user app' | sed 's/sanitize-payload //; s/#[0-9a-f]*/#해시/')"
check_all; echo "  게이트 종료 코드 $?"

echo "## 2. 최소 권한으로 고치기"
AD ACL SETUSER default off >/dev/null
AD ACL SETUSER app resetkeys '~app:*' resetchannels -@all +get +set +del +expire +ttl >/dev/null
AD ACL SETUSER reader resetkeys '~app:*' resetchannels -@all +get +mget >/dev/null
AD ACL LOG RESET >/dev/null
echo "  인증 없이 접속(default 사용자): $(R GET app:1)"
echo "  app 사용자가 ACL LIST 실행: $(RU app ACL LIST)"

echo "## 3. 같은 표로 다시 검사"
check_all; echo "  게이트 종료 코드 $?"

echo "## 4. 교차 확인: ACL DRYRUN(실행하지 않고 판정)과 실제 실행 결과"
for t in "app GET app:1" "app GET other:1" "app FLUSHALL" "reader SET app:1 x"; do
  printf "  DRYRUN %-20s -> %s\n" "$t" "$(AD ACL DRYRUN $t | cut -c1-80)"
done
echo "## 5. ACL LOG: 거부된 시도가 사유와 함께 남음"
AD ACL LOG 20 | awk 'NR%2==1{k=$0} NR%2==0{print "  " k ": " $0}' | grep -E '^  (reason|object|username):' | paste - - - | head -8 | sed 's/\t/  /g'
AD INFO server | grep redis_version | tr -d '\r' | sed 's/^/  /'
docker rm -f $N >/dev/null 2>&1
echo "## 끝"
