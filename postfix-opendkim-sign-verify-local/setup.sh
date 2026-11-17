#!/bin/sh
# 전용 네트워크와 컨테이너 세 개(보내는 서버, 시험 DNS, 받는 서버)를 만듭니다.
export MSYS_NO_PATHCONV=1
set -e
docker build -q -t cr-fx-mail:latest . >/dev/null && echo built
docker network create --internal --subnet 10.89.118.0/24 cr-fx-net

# 1) 보내는 서버: 기동하면서 키 쌍을 만듭니다.
docker run -d --name cr-fx-send --network cr-fx-net --ip 10.89.118.11 cr-fx-mail:latest send
until docker exec cr-fx-send test -f /etc/opendkim/keys/example.internal/s2026a.txt; do sleep 1; done

# 2) 공개키를 TXT 레코드로 만들어 시험 DNS 에 넣습니다.
docker exec cr-fx-send cat /etc/opendkim/keys/example.internal/s2026a.txt | python mkdns.py > dkim-txt.conf
docker create --name cr-fx-dns --network cr-fx-net --ip 10.89.118.10 cr-fx-mail:latest dns
docker cp dkim-txt.conf cr-fx-dns:/etc/dkim-txt.conf
docker start cr-fx-dns
rm -f dkim-txt.conf

# 3) 받는 서버
docker run -d --name cr-fx-recv --network cr-fx-net --ip 10.89.118.12 cr-fx-mail:latest recv
sleep 5
docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}' --filter name=cr-fx
