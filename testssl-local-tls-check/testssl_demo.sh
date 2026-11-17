#!/usr/bin/env bash
# testssl.sh 로 TLS 설정을 점검한다. 일부러 약하게 만든 nginx(bad)와 고친 nginx(good)를 같은 도구로 비교한다.
# 준비: Docker, 같은 폴더에 nginx_bad.conf, nginx_good.conf, testssl_summary.py. 내 컴퓨터의 컨테이너만 검사한다.
# 실행(Git Bash): bash testssl_demo.sh   (약 3분)
export MSYS_NO_PATHCONV=1
HERE="$(pwd)"
NET=osk-tls
TS="docker run --rm --network $NET drwetter/testssl.sh --color 0 --quiet --warnings off"

cleanup() {
  docker rm -f osk-tls-bad osk-tls-good >/dev/null 2>&1
  docker volume rm osk-tls-certs >/dev/null 2>&1
  docker network rm $NET >/dev/null 2>&1
}
cleanup
docker network create $NET >/dev/null
docker volume create osk-tls-certs >/dev/null

echo "## 1. 인증서 두 장 만들기(나쁜 것: RSA 1024 + SHA1 + SAN 없음 / 좋은 것: ECDSA P-256 + SHA256 + SAN)"
docker run --rm --entrypoint sh -v osk-tls-certs:/certs alpine/openssl -c '
openssl req -x509 -newkey rsa:1024 -sha1 -nodes -days 30 -subj "/CN=bad.lab" \
  -keyout /certs/bad.key -out /certs/bad.crt 2>/dev/null
openssl req -x509 -newkey ec -pkeyopt ec_paramgen_curve:prime256v1 -sha256 -nodes -days 90 \
  -subj "/CN=good.lab" -addext "subjectAltName=DNS:good.lab" \
  -keyout /certs/good.key -out /certs/good.crt 2>/dev/null
chmod 644 /certs/*'
for n in bad good; do
  docker run -d --name osk-tls-$n --network $NET --network-alias $n.lab \
    -v osk-tls-certs:/certs:ro -v "$HERE/nginx_$n.conf:/etc/nginx/conf.d/default.conf:ro" nginx:alpine >/dev/null
done
sleep 3

echo "## 2. 다른 도구(openssl s_client)로 먼저 확인: 어떤 프로토콜이 열려 있나"
for h in bad good; do
  for p in tls1 tls1_1 tls1_2 tls1_3; do
    r=$(docker run --rm --network $NET --entrypoint sh alpine/openssl -c \
      "echo | openssl s_client -connect $h.lab:443 -$p -cipher 'ALL:@SECLEVEL=0' 2>&1 | grep -E 'Protocol  *:|Cipher is' | head -2 | tr -s ' ' | tr '\n' ' '")
    printf '  %-5s %-7s %s\n' "$h" "$p" "$r"
  done
done

echo "## 3. testssl.sh 프로토콜 검사(-p)"
for n in bad good; do
  echo "  [$n]"
  $TS -p $n.lab:443 2>&1 | grep -E '^ (SSLv|TLS 1)' | sed 's/^/  /'
done

echo "## 4. 전체 검사(-p -S -U -h)를 JSON 으로 저장"
mkdir -p out
for n in bad good; do
  SECONDS=0
  docker run --rm --network $NET -v "$HERE/out:/data" drwetter/testssl.sh     --color 0 --quiet --warnings off -p -S -U -h --jsonfile /data/$n.json $n.lab:443 >/dev/null 2>&1
  echo "  $n: ${SECONDS}s"
done

echo "## 5. 심각도별 개수와 LOW 이상 지적"
python testssl_summary.py out/bad.json out/good.json --fail-on HIGH
echo "exit code = $?"

echo "## 6. 실습용 자체 서명 인증서에서 나오는 세 항목만 예외로 두고 기준(HIGH) 적용"
IGN=cert_chain_of_trust,cert_revocation,DNS_CAArecord
for n in bad good; do
  python testssl_summary.py out/$n.json --fail-on HIGH --ignore $IGN --show HIGH | tail -n +1
  echo "  -> $n exit code = ${PIPESTATUS[0]}"
done

echo "## 7. 정리"
cleanup
rm -rf out
docker ps -a --format '{{.Names}}' | grep -c osk-tls
