#!/bin/bash
# 연습용 문자열이 ~/.hermes 안 어느 파일에 남아 있는지 찾습니다. 컨테이너 안에서 실행합니다.
# 사용법: find-secret.sh 찾을문자열
set -e
if [ -z "$1" ]; then
  echo "사용법: find-secret.sh 찾을문자열"
  exit 1
fi
echo "== 찾는 문자열이 든 파일"
grep -rlF "$1" "$HOME/.hermes" 2>/dev/null || echo "(없음)"
