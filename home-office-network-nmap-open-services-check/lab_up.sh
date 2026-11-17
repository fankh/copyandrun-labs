#!/bin/sh
# 연습용 사무실 망을 만듭니다. 사용법: sh lab_up.sh before   (조치 후: sh lab_up.sh after)
MODE=${1:-before}
docker network inspect cr-p24-net >/dev/null 2>&1 || docker network create --subnet 192.168.88.0/24 cr-p24-net
docker image inspect cr-p24-device >/dev/null 2>&1 || docker build -q -t cr-p24-device .

# 기기 하나를 새로 띄웁니다: 이름, 주소, 포트 목록
dev() {
  name=$1; ip=$2; shift 2
  docker rm -f "$name" >/dev/null 2>&1
  case "$name" in
    cr-p24-router) pub="-p 127.0.0.1:18190:80" ;;
    *) pub="" ;;
  esac
  docker run -d --name "$name" --network cr-p24-net --ip "$ip" $pub cr-p24-device "$@" >/dev/null
}

if [ "$MODE" = "before" ]; then
  dev cr-p24-printer 192.168.88.10 631:printer 9100:tcp
  dev cr-p24-nas     192.168.88.20 21:ftp 445:tcp
  dev cr-p24-router  192.168.88.30 80:router 23:telnet
else
  # 조치 후: 프린터 9100, NAS FTP, 라우터 telnet 을 끕니다.
  dev cr-p24-printer 192.168.88.10 631:printer
  dev cr-p24-nas     192.168.88.20 445:tcp
  dev cr-p24-router  192.168.88.30 80:router
fi

# 일반 PC: 열린 서비스가 없는 기기
docker inspect cr-p24-pc >/dev/null 2>&1 || docker run -d --name cr-p24-pc --network cr-p24-net --ip 192.168.88.40 --entrypoint sleep cr-p24-device 3600 >/dev/null
docker ps --filter name=cr-p24- --format 'table {{.Names}}\t{{.Ports}}'
