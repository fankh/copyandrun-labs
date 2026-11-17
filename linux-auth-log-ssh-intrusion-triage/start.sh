#!/bin/sh
# 연습용 서버를 띄웁니다. 시험 계정 deploy 의 비밀번호는 연습용 값입니다.
useradd -m -s /bin/bash deploy
echo 'deploy:Lab-Pass-2026' | chpasswd
usermod -aG sudo deploy
mkdir -p /run/sshd
rsyslogd
exec /usr/sbin/sshd -D
