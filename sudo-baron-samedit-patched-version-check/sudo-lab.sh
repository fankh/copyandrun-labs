#!/bin/sh
# 사용: sh sudo-lab.sh
# 우분투 20.04 컨테이너에 sudo 를 설치하고 같은 폴더의 sudo-check.sh 를 실행한다.
# Git Bash 에서는 경로 변환을 끈다.
export MSYS_NO_PATHCONV=1
docker run --rm -v "$(pwd)":/w ubuntu:20.04 sh -c "apt-get update -qq >/dev/null 2>&1; DEBIAN_FRONTEND=noninteractive apt-get install -y -qq sudo >/dev/null 2>&1; sh /w/sudo-check.sh"
