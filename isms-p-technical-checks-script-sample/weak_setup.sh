#!/bin/sh
# 연습용으로 일부러 허술하게 만든 서버 상태입니다. 실제 서버에 그대로 쓰지 않습니다.
set -e

# 계정: 퇴사자와 시험용 계정이 로그인 셸과 함께 남아 있고, 하나는 비밀번호가 비어 있습니다.
useradd -m -s /bin/bash ops
useradd -m -s /bin/bash retired-kim
echo 'retired-kim:Old-Pass-2024' | chpasswd
useradd -m -s /bin/bash test
passwd -d test >/dev/null
echo 'ops:Lab-Pass-2026' | chpasswd

# 비밀번호 정책: 만료 없음, 최소 길이 없음
sed -i 's/^PASS_MAX_DAYS.*/PASS_MAX_DAYS\t99999/' /etc/login.defs

# TLS: 자체 서명 인증서, TLS 1.0 부터 허용
openssl req -x509 -newkey rsa:2048 -nodes -days 30 -subj "/CN=lab.example.test" \
  -keyout /etc/ssl/private/lab.key -out /etc/ssl/certs/lab.crt 2>/dev/null
cat > /etc/nginx/conf.d/lab.conf <<'CONF'
server {
    listen 443 ssl;
    server_name lab.example.test;
    ssl_certificate /etc/ssl/certs/lab.crt;
    ssl_certificate_key /etc/ssl/private/lab.key;
    ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
    ssl_ciphers ALL:@SECLEVEL=0;
    access_log /var/log/nginx/access.log;
    location / { return 200 "ok\n"; }
}
CONF
rm -f /etc/nginx/sites-enabled/default

# 접근 로그: 누구나 쓸 수 있는 권한, 7일만 보관
touch /var/log/nginx/access.log
chmod 666 /var/log/nginx/access.log
cat > /etc/logrotate.d/nginx <<'CONF'
/var/log/nginx/*.log {
    daily
    rotate 7
    compress
    missingok
}
CONF

# 저장 데이터: 평문 파일
mkdir -p /srv/data
cat > /srv/data/members.csv <<'CSV'
name,phone
Hong Gildong,010-0000-0001
Kim Chulsu,010-0000-0002
Lee Younghee,010-0000-0003
CSV
