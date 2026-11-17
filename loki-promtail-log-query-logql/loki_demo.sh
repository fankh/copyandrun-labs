#!/usr/bin/env bash
# nginx 접근 로그 하나를 Promtail 두 설정(나쁜 라벨과 원문 저장, 좋은 라벨과 마스킹)으로 Loki 두 개에 보내고 같은 점검을 돌린다.
# 준비: Docker, python, 같은 폴더에 loki_*.yaml, promtail_*.yaml, nginx_lab.conf, lbc_check.py. 내 PC의 컨테이너만 쓴다.
# 실행(Git Bash): bash loki_demo.sh   (약 2분). KEEP=1 로 실행하면 컨테이너를 남기고, loki_peek.sh 가 보고 지운다.
export MSYS_NO_PATHCONV=1
HERE="$(pwd)"
OUT=../osk-lbc-out                       # 결과 폴더는 설정 폴더 밖에 둔다
rm -rf "$OUT"; mkdir -p "$OUT/logs"; ABS="$(cd "$OUT" && pwd)"
N=osk-lbc-net
cleanup() { docker rm -f osk-lbc-web osk-lbc-loki-bad osk-lbc-loki-good osk-lbc-pt-bad osk-lbc-pt-good osk-lbc-ca osk-lbc-cb >/dev/null 2>&1; docker network rm $N >/dev/null 2>&1; }
cleanup
docker network create $N >/dev/null
for v in bad good; do
  docker run -d --name osk-lbc-loki-$v --network $N -v "$HERE/loki_$v.yaml:/etc/loki/local.yaml:ro" \
    grafana/loki:3.5.0 -config.file=/etc/loki/local.yaml >/dev/null
done
docker run -d --name osk-lbc-web --network $N -v "$HERE/nginx_lab.conf:/etc/nginx/conf.d/default.conf:ro" \
  -v "$ABS/logs:/var/log/nginx" nginx:alpine >/dev/null
sleep 2
for v in bad good; do
  docker run -d --name osk-lbc-pt-$v --network $N -v "$HERE/promtail_$v.yaml:/etc/promtail/config.yml:ro" \
    -v "$ABS/logs:/var/log/nginx:ro" grafana/promtail:3.5.0 -config.file=/etc/promtail/config.yml >/dev/null
done
echo "## 1. Loki 준비 기다리기"
for v in bad good; do
  for i in $(seq 1 40); do
    r=$(docker run --rm --network $N curlimages/curl -s http://osk-lbc-loki-$v:3100/ready)
    [ "$r" = "ready" ] && break; sleep 3
  done
  echo "  loki-$v: $r"
done

echo "## 2. 트래픽 보내기(클라이언트 A 34건, B 4건, IP를 구분하려고 컨테이너 둘을 유지)"
for c in ca cb; do docker run -d --name osk-lbc-$c --network $N --entrypoint sleep curlimages/curl 600 >/dev/null; done
A() { docker exec osk-lbc-ca curl -s -o /dev/null "$@"; }
B() { docker exec osk-lbc-cb curl -s -o /dev/null "$@"; }
for i in $(seq 1 10); do A http://osk-lbc-web/; done
for i in 1 2 3 4 5; do A "http://osk-lbc-web/search?email=u$i@example.com&token=SECRETtok$i"; done
for i in 1 2 3; do A http://osk-lbc-web/boom; done
for i in $(seq 1 12); do A -X POST -d 'pw=x' http://osk-lbc-web/login; done
for i in 1 2 3 4; do A http://osk-lbc-web/missing; done
for i in 1 2; do B -X POST -d 'pw=x' http://osk-lbc-web/login; B http://osk-lbc-web/boom; done
sleep 12
LINES=$(wc -l < "$ABS/logs/access.log" | tr -d ' ')
E5=$(grep -cE '" 5[0-9][0-9] ' "$ABS/logs/access.log")
echo "  access.log: 전체 $LINES줄, 5xx $E5줄, 이메일이 든 줄 $(grep -c '@example.com' "$ABS/logs/access.log")줄"

echo "## 3. 같은 점검을 두 Loki 에 돌리기(실패 개수가 종료 코드)"
for v in bad good; do
  echo "### $v"
  docker run --rm --network $N -v "$HERE:/w:ro" python:3.12-slim python /w/lbc_check.py http://osk-lbc-loki-$v:3100 --lines "$LINES" --err5xx "$E5" --bf-ip 12
  echo "  종료 코드 $?"
done
[ "$KEEP" = "1" ] || cleanup
echo "## 끝 (결과 폴더: $OUT)"
