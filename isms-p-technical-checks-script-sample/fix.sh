#!/bin/sh
# 점검에서 나온 취약 항목을 고칩니다. 연습용 값이며 실제 서버에서는 절차와 승인에 맞춰 적용합니다.
set -e

# 계정: 퇴사자 계정 잠금과 로그인 셸 제거, 시험 계정 삭제
usermod -L -s /usr/sbin/nologin retired-kim
userdel -r test 2>/dev/null || true

# 비밀번호 정책: 90일 만료와 pam_pwquality 의 최소 길이 12 (여기서는 설정 파일 값만 둡니다)
sed -i 's/^PASS_MAX_DAYS.*/PASS_MAX_DAYS\t90/' /etc/login.defs
chage -M 90 ops
mkdir -p /etc/security
echo 'minlen = 12' > /etc/security/pwquality.conf

# TLS: 1.2 이상만 허용
sed -i 's/^\s*ssl_protocols.*/    ssl_protocols TLSv1.2 TLSv1.3;/; s/^\s*ssl_ciphers.*/    ssl_ciphers HIGH:!aNULL:!MD5;/' /etc/nginx/conf.d/lab.conf
nginx -t && nginx -s reload

# 접근 로그: 640 권한, 365일 보관
chown root:adm /var/log/nginx/access.log
chmod 640 /var/log/nginx/access.log
sed -i 's/rotate 7/rotate 365/' /etc/logrotate.d/nginx

# 저장 데이터: AES-256 으로 암호화하고 평문 원본 삭제 (연습용 암호문구)
LAB_PASS=lab-only-passphrase openssl enc -aes-256-cbc -pbkdf2 -salt -pass env:LAB_PASS \
  -in /srv/data/members.csv -out /srv/data/members.csv.enc
rm -f /srv/data/members.csv
echo fixed
