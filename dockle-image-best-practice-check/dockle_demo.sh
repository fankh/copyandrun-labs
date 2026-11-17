#!/usr/bin/env bash
# Dockle 로 "만들어진 이미지"의 모범 사례 위반을 점검한다. 일부러 나쁘게 만든 이미지(bad)와 고친 이미지(good)를 비교한다.
# 준비: Docker, 같은 폴더에 Dockerfile.bad, Dockerfile.good, app.py. 내 컴퓨터에서 만든 이미지만 검사한다.
# 실행(Git Bash): bash dockle_demo.sh   (약 1분)
export MSYS_NO_PATHCONV=1
# Dockle 은 이미지를 읽으려고 Docker 소켓을 마운트한다. --no-color 로 색 코드를 끈다
DK="docker run --rm -v /var/run/docker.sock:/var/run/docker.sock goodwithtech/dockle:latest --no-color"

echo "## 1. 이미지 두 개 만들기(태그를 꼭 붙인다. 태그가 없으면 latest 로 보고 경고한다)"
docker build -q -f Dockerfile.bad  -t osk-dockle-bad:1  . >/dev/null
docker build -q -f Dockerfile.good -t osk-dockle-good:1 . >/dev/null
$DK --version

echo "## 2. 나쁜 이미지를 그대로 검사: 앞 한 줄씩만(긴 줄은 자른다)"
$DK osk-dockle-bad:1 2>&1 | grep -E '^(FATAL|WARN|INFO)' | cut -c1-110

echo "## 3. DKL-DI-0004 는 내 Dockerfile 이 아니라 베이스 이미지(python:3.12-alpine)의 빌드 기록에서 나온다. 예외로 두고 JSON 으로 본다"
$DK -i DKL-DI-0004 -f json osk-dockle-bad:1 2>/dev/null | python -X utf8 -c "
import json, sys
d = json.load(sys.stdin)
print('summary:', d['summary'])
for x in d['details']:
    print(f\"  {x['level']:6} {x['code']:11} {x['alerts'][0][:70]}\")"

echo "## 4. 실패 기준(--exit-level)에 따른 종료 코드. 예외: DKL-DI-0004"
for lv in fatal warn info; do
  for n in bad good; do
    $DK -i DKL-DI-0004 --exit-code 1 --exit-level $lv osk-dockle-$n:1 >/dev/null 2>&1
    echo "  level=$lv  $n  exit=$?"
  done
done

echo "## 5. 왜 ENV 의 비밀이 문제인가: 이미지 기록을 읽기만 해도 값이 보인다"
docker history --no-trunc --format '{{.CreatedBy}}' osk-dockle-bad:1 | grep -o 'DB_PASSWORD=[^ ]* API_TOKEN=[^ ]*' | head -1
docker run --rm osk-dockle-bad:1 id

echo "## 6. 고친 이미지: 비밀은 이미지에 넣지 않고, 일반 사용자로 실행하고, HEALTHCHECK 를 둔다"
docker run --rm osk-dockle-good:1 id
docker inspect --format 'healthcheck: {{.Config.Healthcheck.Test}}' osk-dockle-good:1
$DK -i DKL-DI-0004 osk-dockle-good:1 2>&1 | grep -E '^(FATAL|WARN|INFO)' | cut -c1-110

echo "## 7. 남은 INFO(CIS-DI-0005, 콘텐츠 신뢰)는 빌드 환경의 설정이라 이 이미지에서는 예외로 두고 기준을 INFO 로 둔다"
$DK -i DKL-DI-0004 -i CIS-DI-0005 --exit-code 1 --exit-level info osk-dockle-good:1 >/dev/null 2>&1
echo "  good, level=info, 예외 2개: exit=$?"

echo "## 8. 정리"
docker rmi osk-dockle-bad:1 osk-dockle-good:1 >/dev/null
docker images --format '{{.Repository}}' | grep -c osk-dockle
