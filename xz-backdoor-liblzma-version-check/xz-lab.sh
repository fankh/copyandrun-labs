#!/bin/sh
# 사용: sh xz-lab.sh
# 우분투 22.04 컨테이너에 xz-utils 와 openssh-server 를 설치하고 같은 폴더의 xz-check.sh 를 실행한다.
# 이어서 경계 버전(5.4.6, 5.6.0, 5.6.1, 5.6.2)의 판정도 확인한다.
# Git Bash 에서는 경로 변환을 끈다.
export MSYS_NO_PATHCONV=1
docker run --rm -v "$(pwd)":/w ubuntu:22.04 sh -c "apt-get update -qq >/dev/null 2>&1; DEBIAN_FRONTEND=noninteractive apt-get install -y -qq xz-utils openssh-server >/dev/null 2>&1; echo '== 설치된 xz'; sh /w/xz-check.sh; for v in 5.4.6 5.6.0 5.6.1 5.6.2; do echo \"== 시험 버전 \$v\"; sh /w/xz-check.sh \$v | sed -n '2p'; done"
