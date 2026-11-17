#!/bin/sh
# 연습용 컨테이너, 이미지, 네트워크를 지웁니다.
docker rm -f cr-p24-printer cr-p24-nas cr-p24-router cr-p24-pc cr-p24-scan >/dev/null 2>&1
docker network rm cr-p24-net
docker rmi cr-p24-device
