#!/bin/bash
# 제목에 키워드가 든 세션을 지우고, 입력 기록 파일을 비우고, 저장소를 정리합니다.
# 대시보드와 게이트웨이가 저장소를 쓰고 있으면 정리가 거부되므로 먼저 멈춥니다.
# 컨테이너 안에서 실행합니다. 사용법: forget-session.sh 제목키워드
if [ -z "$1" ]; then
  echo "사용법: forget-session.sh 제목키워드"
  exit 1
fi
hermes dashboard --stop > /dev/null 2>&1
hermes gateway stop > /dev/null 2>&1
sleep 3
for id in $(hermes sessions list | grep -F "$1" | awk '{print $NF}'); do
  hermes sessions delete --yes "$id"
done
hermes sessions optimize
: > "$HOME/.hermes/.hermes_history"
echo "정리 끝"
