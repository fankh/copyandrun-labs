#!/usr/bin/env bash
# Nmap 심화: 서비스 세 개가 있는 시험 네트워크에서 호스트 찾기, 전체 포트, 서비스 식별, XML 결과 집계.
# 내가 만든 컨테이너만 대상으로 한다. 다른 사람의 서버에는 허락 없이 실행하지 않는다.
# 준비: Docker, 파이썬(XML 집계용)
# 실행(Git Bash): bash scan_more.sh   (약 3분)
set -u
export MSYS_NO_PATHCONV=1
NET=lab-net2
NMAP="docker run --rm --network $NET instrumentisto/nmap:latest"

docker rm -f lab-web lab-redis lab-pg >/dev/null 2>&1
docker network rm $NET >/dev/null 2>&1
docker network create $NET >/dev/null
docker run -d --name lab-web   --network $NET nginx:alpine >/dev/null
docker run -d --name lab-redis --network $NET redis:7-alpine >/dev/null
docker run -d --name lab-pg    --network $NET -e POSTGRES_PASSWORD=lab-only postgres:16-alpine >/dev/null
sleep 12
SUBNET=$(docker network inspect $NET -f '{{(index .IPAM.Config 0).Subnet}}')
RANGE="${SUBNET%.*.*}.0.0/24"                # 도커가 주는 /16 전체(6만 5천 개 주소)는 너무 오래 걸려 앞의 /24 만 훑는다
echo "시험 네트워크 $NET ($SUBNET), 훑는 범위 $RANGE"

echo "## 1. 호스트 찾기(-sn): 대역 안에서 응답하는 주소"
$NMAP -sn $RANGE 2>&1 | grep -E 'Nmap scan report|Host is up|Nmap done' | sed 's/([0-9.]*)//'

echo "## 2. 컨테이너별 열린 포트(-p- 전체 65535개, -sV 서비스 식별, XML 로 저장)"
for h in lab-web lab-redis lab-pg; do
  $NMAP -p- -sV -T4 -oX - $h 2>/dev/null > "scan-$h.xml"
done
python -X utf8 - <<'PY'
import xml.etree.ElementTree as ET
for h in ("lab-web", "lab-redis", "lab-pg"):
    r = ET.parse(f"scan-{h}.xml").getroot()
    ex = [e.get("count") for e in r.iter("extraports")]
    sec = r.find("runstats/finished").get("elapsed")
    print(f"{h:<10} {sec:>6}초 닫힌 포트 {ex[0] if ex else '0'}개")
    for p in r.iter("port"):
        s = p.find("service")
        print(f"           {p.get('portid')}/{p.get('protocol')} {p.find('state').get('state')} {s.get('name')} {s.get('product', '')} {s.get('version', '')}".rstrip())
PY

echo "## 3. 닫힌 포트의 사유(--reason): 열린 곳과 닫힌 곳이 어떻게 다르게 응답하나"
$NMAP -p 80,6379,9999 --reason lab-web 2>&1 | grep -E '^[0-9]+/'

echo "## 4. 정리"
docker rm -f lab-web lab-redis lab-pg >/dev/null
docker network rm $NET >/dev/null
rm -f scan-lab-*.xml
docker ps -a --filter name=lab- --format '{{.Names}}' | wc -l | sed 's/^/남은 컨테이너 /'
