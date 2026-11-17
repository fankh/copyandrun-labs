#!/usr/bin/env bash
# 도커 전용 네트워크에 시험용 nginx 를 띄워 Nmap 으로 점검하고, 끝나면 전부 지운다.
# 내가 만든 컨테이너만 대상으로 한다. 다른 사람의 서버에는 허락 없이 실행하지 않는다.
# 실행: bash scan_lab.sh
set -u
NET=lab-net
NMAP="docker run --rm --network $NET instrumentisto/nmap:latest"

docker network create $NET >/dev/null
docker run -d --name lab-web --network $NET nginx:alpine >/dev/null
sleep 5

echo "## 1. 1~1024번 포트"
$NMAP -p 1-1024 lab-web 2>&1 | grep -E 'Nmap scan|Not shown|PORT|open|Nmap done'

echo "## 2. 서비스 버전(-sV)"
$NMAP -sV -p 80 lab-web 2>&1 | grep -E 'PORT|open|Nmap done'

echo "## 3. 스크립트(http-title, http-headers)"
$NMAP -p 80 --script http-title,http-headers lab-web 2>&1 | grep -E 'open|Server:|Content-Type|http-title'

docker rm -f lab-web >/dev/null
docker network rm $NET >/dev/null
echo "## 정리 완료: 컨테이너와 네트워크를 지웠습니다"
