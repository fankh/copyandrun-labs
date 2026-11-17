#!/usr/bin/env bash
# docker-compose.yml 용 정책(Rego)을 시험하고, 약한 파일, 경고만 있는 파일, 고친 파일에 적용하고, 막으려던 위험이 진짜인지 확인한다.
# 준비: Docker, 같은 폴더에 compose.rego, compose_test.rego, compose.bad.yml, compose.warn.yml, compose.good.yml.
# 실행(Git Bash): bash conftest_demo.sh   (약 1분)
export MSYS_NO_PATHCONV=1
HERE="$(pwd)"
CT() { docker run --rm -v "$HERE:/p:ro" -w /p openpolicyagent/conftest "$@"; }
cleanup() { docker rm -f osk-fc-victim >/dev/null 2>&1; }
cleanup

echo "## 1. 정책 단위 시험(conftest verify)"
CT verify -p . --no-color 2>&1 | tail -1

echo "## 2. 세 파일에 정책 적용"
for f in bad warn good; do
  echo "[compose.$f.yml]"
  CT test compose.$f.yml -p . --no-color 2>&1 | grep -E '^(FAIL|WARN)|tests,' | sed -E 's/ - compose\.[a-z]+\.yml - main - / /; s/^/  /'
  CT test compose.$f.yml -p . --no-color >/dev/null 2>&1; a=$?
  CT test compose.$f.yml -p . --no-color --fail-on-warn >/dev/null 2>&1; b=$?
  echo "  종료 코드: 기본 $a, --fail-on-warn $b"
done

echo "## 3. 교차 확인: docker.sock 마운트가 왜 위험한가"
docker run -d --name osk-fc-victim --entrypoint sleep alpine 600 >/dev/null
echo -n "  소켓 마운트 없음:  "; docker run --rm docker:cli docker ps --filter name=osk-fc-victim --format '{{.Names}}' 2>&1 | cut -c1-48
echo -n "  소켓 마운트 있음:  "; docker run --rm -v /var/run/docker.sock:/var/run/docker.sock docker:cli docker ps --filter name=osk-fc-victim --format '{{.Names}}'
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock docker:cli docker stop osk-fc-victim >/dev/null
echo "  마운트한 컨테이너가 다른 컨테이너를 멈춘 뒤 상태: $(docker inspect -f '{{.State.Status}}' osk-fc-victim)"
cleanup
echo "## 끝"
