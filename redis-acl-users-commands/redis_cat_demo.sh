#!/usr/bin/env bash
# 명령 묶음(@read, @write, @dangerous)으로 허용 목록을 짧게 쓰는 방법을 확인한다.
# 실행(Git Bash): bash redis_cat_demo.sh   (약 10초)
export MSYS_NO_PATHCONV=1
N=osk-fb-redis2
docker rm -f $N >/dev/null 2>&1
docker run -d --name $N redis:7-alpine >/dev/null
sleep 2
R() { docker exec $N redis-cli --no-auth-warning "$@" 2>&1; }
echo "## 묶음별 명령 수"
for c in read write dangerous; do echo "  @$c: $(R ACL CAT $c | wc -l)개"; done
echo "  @dangerous 안의 예: $(R ACL CAT dangerous | grep -E '^(flushall|keys|config|shutdown|debug)$' | tr '\n' ' ')"
echo "## +@read -@dangerous 로 만든 사용자"
R ACL SETUSER viewer on '>lab' '~v:*' -@all +@read -@dangerous >/dev/null
R SET v:1 hello >/dev/null
RV() { docker exec $N redis-cli --no-auth-warning --user viewer --pass lab "$@" 2>&1; }
for cmd in "GET v:1" "MGET v:1 v:2" "SET v:1 x" "KEYS v:*" "INFO"; do
  printf "  %-14s -> %s\n" "$cmd" "$(RV $cmd | head -1 | cut -c1-70)"
done
echo "  DRYRUN viewer SCAN 0 -> $(R ACL DRYRUN viewer SCAN 0)"
docker rm -f $N >/dev/null 2>&1
echo "## 끝"
