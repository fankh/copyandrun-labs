#!/bin/sh
# 컨테이너 안에서 실행: 내 CA를 만들고, 서버 인증서 여러 개를 만든 뒤 openssl verify 로 기대한 결과와 비교한다.
cd /w
FAIL=0
# --- 1. 루트 CA(10년) ---
openssl req -x509 -newkey rsa:3072 -nodes -keyout ca.key -out ca.crt -days 3650 -subj "/CN=Lab Root CA/O=copyandrun lab" \
  -addext "basicConstraints=critical,CA:true,pathlen:0" -addext "keyUsage=critical,keyCertSign,cRLSign" 2>/dev/null
# 아무 관계 없는 다른 CA(신뢰하지 않는 쪽)
openssl req -x509 -newkey rsa:2048 -nodes -keyout evil.key -out evil.crt -days 3650 -subj "/CN=Other CA" \
  -addext "basicConstraints=critical,CA:true" 2>/dev/null

# --- 2. 서버 인증서 만들기: leaf <이름> <SAN 줄> <EKU> <CA키> <CA인증서> ---
leaf() {
  openssl req -newkey rsa:2048 -nodes -keyout "$1.key" -out "$1.csr" -subj "/CN=$2" 2>/dev/null
  { [ -n "$3" ] && echo "subjectAltName=$3"
    echo "basicConstraints=critical,CA:false"; echo "keyUsage=critical,digitalSignature,keyEncipherment"
    [ -n "$4" ] && echo "extendedKeyUsage=$4"; } > "$1.ext"
  openssl x509 -req -in "$1.csr" -CA "$5" -CAkey "$6" -CAcreateserial -out "$1.crt" -days 365 -sha256 -extfile "$1.ext" 2>/dev/null
}
leaf good     web.lab "DNS:web.lab,DNS:www.lab" serverAuth ca.crt ca.key
leaf nosan    web.lab ""                        serverAuth ca.crt ca.key
leaf clientek web.lab "DNS:web.lab"             clientAuth ca.crt ca.key
leaf foreign  web.lab "DNS:web.lab"             serverAuth evil.crt evil.key

# --- 3. 검증: check <설명> <기대: ok|fail> <openssl verify 인자...> ---
check() {
  desc="$1"; want="$2"; shift 2
  out=$(openssl verify "$@" 2>&1); rc=$?
  got=ok; [ $rc -ne 0 ] && got=fail
  reason=$(echo "$out" | grep -E 'error [0-9]+|OK|Hostname|mismatch|mismatch' | head -2 | tr '\n' ' ' | sed 's/^ *//')
  mark=맞음; [ "$got" != "$want" ] && { mark=어긋남; FAIL=1; }
  printf '  %-34s 기대 %-4s 결과 %-4s %s  %s\n' "$desc" "$want" "$got" "$mark" "$reason"
}
LATE=$(( $(date +%s) + 400*86400 ))
check "정상(이름 web.lab)"                 ok   -CAfile ca.crt -purpose sslserver -verify_hostname web.lab good.crt
check "다른 이름(other.lab)"               fail -CAfile ca.crt -purpose sslserver -verify_hostname other.lab good.crt
check "SAN 없이 CN 만(web.lab)"            ok   -CAfile ca.crt -purpose sslserver -verify_hostname web.lab nosan.crt   # OpenSSL 은 CN 으로 대신 통과시킨다
check "400일 뒤 시각으로 검증(만료)"       fail -CAfile ca.crt -purpose sslserver -attime $LATE good.crt
check "용도가 clientAuth 만"               fail -CAfile ca.crt -purpose sslserver clientek.crt
check "신뢰하지 않는 CA가 서명"            fail -CAfile ca.crt -purpose sslserver foreign.crt
# openssl verify 가 놓치는 부분은 직접 규칙으로 막는다: 서버 인증서에는 SAN 이 있어야 한다.
for f in good nosan; do
  if openssl x509 -in $f.crt -noout -ext subjectAltName 2>/dev/null | grep -q DNS:; then got=ok; else got=fail; fi
  want=ok; [ $f = nosan ] && want=fail
  mark=맞음; [ "$got" != "$want" ] && { mark=어긋남; FAIL=1; }
  printf '  %-34s 기대 %-4s 결과 %-4s %s
' "자체 규칙: $f 에 SAN 이 있는가" $want $got $mark
done
echo "  남은 유효 기간(good): $(openssl x509 -in good.crt -noout -enddate)"
echo "  CA 제약: $(openssl x509 -in ca.crt -noout -ext basicConstraints | tail -1 | sed 's/^ *//')"
exit $FAIL
