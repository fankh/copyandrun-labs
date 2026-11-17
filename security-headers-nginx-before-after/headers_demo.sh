#!/usr/bin/env bash
# nginx 설정 세 가지(헤더 없음, 헤더를 server 에만 둔 설정, 올바른 설정)에서 네 경로의 응답 헤더를 모아 검사한다.
# 준비: Docker, python, 같은 폴더에 bad.conf, naive.conf, good.conf, snippet_headers.conf, hdr_audit.py. 내 PC의 컨테이너에만 요청한다.
# 실행(Git Bash): bash headers_demo.sh   (약 1분)
export MSYS_NO_PATHCONV=1
HERE="$(pwd)"
OUT=../osk-fc-hd-out                     # 결과 폴더는 설정 폴더 밖에 둔다
rm -rf "$OUT"; mkdir -p "$OUT/certs"; ABS="$(cd "$OUT" && pwd)"
cleanup() { docker rm -f osk-fc-hd-bad osk-fc-hd-naive osk-fc-hd-good osk-fc-hd-cli >/dev/null 2>&1; docker network rm osk-fc-hdnet >/dev/null 2>&1; }
cleanup
docker run --rm -v "$ABS/certs:/c" --entrypoint sh alpine/openssl -c \
  'openssl req -x509 -newkey rsa:2048 -nodes -keyout /c/tls.key -out /c/tls.crt -days 2 -subj /CN=hd.lab >/dev/null 2>&1'
docker network create osk-fc-hdnet >/dev/null
for n in bad naive good; do
  docker run -d --name osk-fc-hd-$n --network osk-fc-hdnet \
    -v "$HERE/$n.conf:/etc/nginx/conf.d/default.conf:ro" \
    -v "$HERE/snippet_headers.conf:/etc/nginx/snippets/security_headers.conf:ro" \
    -v "$ABS/certs:/certs:ro" nginx:alpine >/dev/null
done
docker run -d --name osk-fc-hd-cli --network osk-fc-hdnet --entrypoint sleep curlimages/curl 3600 >/dev/null
sleep 3
for n in bad naive good; do
  for p in "root:/" "login:/login" "api:/api/x" "missing:/missing"; do
    docker exec osk-fc-hd-cli curl -sk -D - -o /dev/null "https://osk-fc-hd-$n${p#*:}" | tr -d '\r' > "$OUT/${n}__${p%%:*}.hdr"
  done
  python hdr_audit.py "$OUT" $n; echo "  종료 코드 $?"
done
echo "## 교차 확인: testssl.sh --headers 의 서버 배너와 보안 헤더"
for n in bad good; do
  echo "[$n]"; docker run --rm --network osk-fc-hdnet drwetter/testssl.sh --headers --color 0 osk-fc-hd-$n:443 2>&1 \
    | grep -E 'Server banner|Security headers' | sed 's/^ */  /'
done
cleanup
echo "## 끝 (결과 폴더: $OUT)"
