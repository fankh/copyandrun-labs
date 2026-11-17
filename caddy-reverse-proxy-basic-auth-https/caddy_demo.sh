#!/usr/bin/env bash
# Caddy 를 앞에 두고 뒤의 nginx 를 감싸는 시험: 자체 HTTPS, 기본 인증, 보안 헤더, HTTP 리다이렉트, 접속 기록.
# 준비: Docker, curl, openssl(없으면 4번을 건너뛴다). 모든 컨테이너는 이 PC 안(127.0.0.1)에서만 열린다.
# 주의: osk-caddy, osk-app 컨테이너와 osk-net-caddy 네트워크, osk_caddy_data 볼륨을 만들고 끝에서 지운다.
# 실행(Git Bash): bash caddy_demo.sh   (약 1분)
set -u
export MSYS_NO_PATHCONV=1
HERE="$(pwd -W 2>/dev/null || pwd)"
NET=osk-net-caddy
PW="lab-only-pass"                                   # 실습용 값. 실제 비밀번호를 쓰지 않는다
H=https://localhost:8443

docker rm -f osk-caddy osk-app >/dev/null 2>&1; docker network rm $NET >/dev/null 2>&1; docker volume rm osk_caddy_data >/dev/null 2>&1
docker network create $NET >/dev/null
docker run -d --name osk-app --network $NET nginx:alpine >/dev/null          # 뒤쪽 앱: 바깥으로 포트를 열지 않는다

echo "## 1. 비밀번호 해시 만들기(caddy hash-password)"
HASH=$(docker run --rm caddy:2 caddy hash-password --plaintext "$PW")
echo "해시 앞부분: ${HASH:0:7}... (bcrypt, 길이 ${#HASH})"

cat > Caddyfile <<CF
{
	auto_https disable_redirects
}
localhost:443 {
	tls internal
	basic_auth {
		admin $HASH
	}
	header {
		Strict-Transport-Security "max-age=31536000"
		X-Content-Type-Options nosniff
		-Server
	}
	log {
		output stdout
		format json
	}
	reverse_proxy osk-app:80
}
http://localhost:80 {
	redir https://localhost:8443{uri} permanent
}
CF
docker run -d --name osk-caddy --network $NET -p 127.0.0.1:8443:443 -p 127.0.0.1:8480:80 \
  -v "$HERE/Caddyfile:/etc/caddy/Caddyfile:ro" -v osk_caddy_data:/data caddy:2 >/dev/null
for i in $(seq 1 30); do [ "$(curl -sk -o /dev/null -w '%{http_code}' $H/)" = 401 ] && break; sleep 1; done

SINCE=$(date +%s)                                       # 이 시각(초) 이후의 접속만 7번에서 센다
echo "## 2. 인증: 없을 때, 틀렸을 때, 맞을 때"
printf '자격 증명 없음   '; curl -sk -o /dev/null -w '%{http_code}\n' $H/
printf '틀린 비밀번호    '; curl -sk -o /dev/null -w '%{http_code}\n' -u admin:wrong $H/
printf '맞는 비밀번호    '; curl -sk -o /dev/null -w '%{http_code}\n' -u admin:$PW $H/
printf '맞는 비밀번호 본문 '; curl -sk -u admin:$PW $H/ | grep -o '<title>[^<]*</title>'

echo "## 3. 응답 헤더(보안 헤더가 붙고 Server 헤더는 빠졌는가)"
curl -sk -I -u admin:$PW $H/ | tr -d '\r' | grep -i -E '^(HTTP|strict-transport|x-content|server|www-authenticate)' 
printf '인증 실패 시 헤더: '; curl -sk -I $H/ | tr -d '\r' | grep -i www-authenticate

echo "## 4. 인증서: 누가 발급했나(자체 CA)"
echo | openssl s_client -connect localhost:8443 -servername localhost 2>/dev/null | openssl x509 -noout -issuer -ext subjectAltName -dates 2>/dev/null | sed 's/^/   /'
printf '검증 없이(-k) 접속   : '; curl -sk -o /dev/null -w '%{http_code}\n' -u admin:$PW $H/
printf '검증하며(-k 없이) 접속: '; curl -s -o /dev/null -w '%{http_code}\n' -u admin:$PW $H/ 2>&1 | head -1; echo "   (curl 종료 코드 ${PIPESTATUS[0]}: 60 이면 인증서를 믿을 수 없다는 뜻)"

echo "## 5. HTTP 로 오면 HTTPS 로 보내는가"
curl -s -o /dev/null -w '%{http_code} %{redirect_url}
' http://localhost:8480/path?x=1 | sed 's/^/상태 코드, 이동 위치: /'

echo "## 6. 뒤쪽 앱은 바깥에서 직접 보이는가"
docker ps --filter name=osk-app --format '앱 컨테이너의 포트 표시(호스트로 나가면 -> 가 붙는다): {{.Ports}}'
printf '컨테이너 이름으로 호스트에서 접속: '; curl -s -m 3 -o /dev/null -w '%{http_code}\n' http://osk-app/ 2>&1 | head -1

echo "## 7. 접속 기록(JSON 로그)에서 상태 코드 세기"
docker logs --since $SINCE osk-caddy 2>&1 | grep '"logger":"http.log.access' | python -X utf8 -c "
import json, sys
from collections import Counter
c = Counter()
for l in sys.stdin:
    j = json.loads(l); c[j['status']] += 1
print('상태 코드별 요청 수', dict(sorted(c.items())))
"

docker rm -f osk-caddy osk-app >/dev/null; docker network rm $NET >/dev/null; docker volume rm osk_caddy_data >/dev/null; rm -f Caddyfile
echo "## 정리: 컨테이너, 네트워크, 볼륨, Caddyfile 삭제"
