#!/usr/bin/env bash
# 내 CA 로 서버 인증서를 발급하고, 정상과 실패 사례 6가지가 기대대로 판정되는지 확인한 뒤 nginx 로 실제 TLS 연결까지 대조한다.
# 준비: Docker, 같은 폴더에 ca_lab.sh. 키는 시험용이고 결과 폴더는 스크립트 폴더 밖에 둔다.
# 실행(Git Bash): bash ca_demo.sh   (약 1분)
export MSYS_NO_PATHCONV=1
HERE="$(pwd)"; OUT=../osk-ca-out
rm -rf "$OUT"; mkdir -p "$OUT"; ABS="$(cd "$OUT" && pwd)"
IMG=alpine/openssl
echo "## 1. 인증서 발급과 verify 6가지"
docker run --rm --entrypoint sh -v "$ABS:/w" -v "$HERE/ca_lab.sh:/ca_lab.sh:ro" $IMG /ca_lab.sh; RC=$?
echo "  게이트 종료 코드: $RC"

echo "## 2. nginx 에 good 인증서를 올리고 s_client 로 연결"
docker rm -f osk-fa-ca-web >/dev/null 2>&1; docker network rm osk-fa-ca-net >/dev/null 2>&1
docker network create osk-fa-ca-net >/dev/null
docker run -d --name osk-fa-ca-web --network osk-fa-ca-net --network-alias web.lab -v "$ABS:/c:ro" nginx:alpine sh -c \
 'printf "server{listen 443 ssl;ssl_certificate /c/good.crt;ssl_certificate_key /c/good.key;location /{return 200 ok;}}" > /etc/nginx/conf.d/default.conf; nginx -g "daemon off;"' >/dev/null
sleep 3
try() { docker run --rm --network osk-fa-ca-net --entrypoint sh -v "$ABS:/w:ro" $IMG -c \
  "echo | openssl s_client -connect web.lab:443 -servername web.lab -CAfile /w/$1 -verify_hostname $2 2>&1 | grep -E 'Verify return code|Verification' | head -1"; }
echo -n "  신뢰하는 CA(ca.crt), 이름 web.lab : "; try ca.crt web.lab
echo -n "  신뢰하는 CA(ca.crt), 이름 other.lab: "; try ca.crt other.lab
echo -n "  다른 CA(evil.crt), 이름 web.lab    : "; try evil.crt web.lab
docker rm -f osk-fa-ca-web >/dev/null; docker network rm osk-fa-ca-net >/dev/null
echo "## 끝 (결과 폴더: $OUT)"
exit $RC
