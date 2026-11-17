#!/bin/sh
# 사용: sh dirtypipe-lab.sh
# 컨테이너는 호스트 커널을 그대로 쓴다. 호스트 커널과 경계값 버전 몇 개를 같은 폴더의 dirtypipe-check.sh 로 점검한다.
# Git Bash 에서는 경로 변환을 끈다.
export MSYS_NO_PATHCONV=1
docker run --rm -v "$(pwd)":/w ubuntu:20.04 sh -c "echo '호스트 커널 확인'; sh /w/dirtypipe-check.sh; echo '경계값 확인'; for v in 5.7.19 5.8.0 5.10.101 5.10.102 5.15.24 5.15.25 5.16.10 5.16.11; do sh /w/dirtypipe-check.sh \$v; done"
