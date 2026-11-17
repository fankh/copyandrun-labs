#!/usr/bin/env bash
# n8n 컨테이너를 띄워 워크플로 두 개를 가져와 게시하고, 호출 결과를 확인한 뒤 모두 지운다.
# 준비: Docker, 이 폴더의 wf.json 과 wf2.json, curl
# 실행(Git Bash): bash run_n8n.sh   (약 2분)
set -u
export MSYS_NO_PATHCONV=1                      # Git Bash 가 /wf 같은 경로를 바꾸지 않게 한다
HERE="$(pwd -W 2>/dev/null || pwd)"            # 윈도우는 C:/... 경로, 리눅스는 그대로
NAME=osk-n8n; PORT=3903; URL=http://127.0.0.1:$PORT
call() { curl -s -w ' [HTTP %{http_code}]\n' "$@"; }

echo "## 1. 실행"
docker run -d --name $NAME -p 127.0.0.1:$PORT:5678 -v osk_n8n:/home/node/.n8n -v "$HERE:/wf" \
  -e N8N_SECURE_COOKIE=false n8nio/n8n:2.45.5 >/dev/null
for i in $(seq 1 60); do
  [ "$(curl -s -o /dev/null -w '%{http_code}' $URL/healthz)" = "200" ] && { echo "/healthz 200 (${i}번째 확인)"; break; }
  sleep 2
done
sleep 20                                       # 첫 실행 직후에는 내부 준비가 끝날 때까지 기다린다
echo "버전 $(docker exec $NAME n8n --version 2>/dev/null | tail -1), 컨테이너 상태: $(docker inspect -f '{{.State.Status}}' $NAME)"

echo "## 2. 가져오기와 게시"
docker exec $NAME n8n import:workflow --input=/wf/wf.json 2>&1 | tail -1
docker exec $NAME n8n import:workflow --input=/wf/wf2.json 2>&1 | tail -1
docker exec $NAME n8n list:workflow 2>/dev/null
docker exec $NAME n8n publish:workflow --id=wfhello0000000001 2>&1 | tail -1
docker exec $NAME n8n publish:workflow --id=wfguard0000000002 2>&1 | tail -1
docker restart $NAME >/dev/null
for i in $(seq 1 60); do
  [ "$(curl -s -o /dev/null -w '%{http_code}' $URL/healthz)" = "200" ] && break
  sleep 2
done
sleep 5

echo "## 3. hello-webhook 호출"
call -X POST -H 'content-type: application/json' -d '{"name":"minsu"}' $URL/webhook/hello
call -X POST -H 'content-type: application/json' -d '{}' $URL/webhook/hello
call $URL/webhook/hello

echo "## 4. guarded-webhook 호출(헤더 x-token 검사)"
call -X POST -H 'content-type: application/json' -H 'x-token: lab-secret' -d '{"text":"hi"}' $URL/webhook/guarded
call -X POST -H 'content-type: application/json' -H 'x-token: wrong' -d '{"text":"hi"}' $URL/webhook/guarded
call -X POST -H 'content-type: application/json' -d '{"text":"hi"}' $URL/webhook/guarded

echo "## 5. 정리"
docker rm -f $NAME >/dev/null && docker volume rm osk_n8n >/dev/null && echo "컨테이너와 볼륨 삭제"
docker ps -a --filter name=$NAME --format '{{.Names}}' | wc -l | sed 's/^/남은 컨테이너 /'
