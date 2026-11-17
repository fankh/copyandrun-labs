#!/bin/sh
# 컨테이너 안에서 실행하는 보완 스크립트. Lynis 제안 중 파일과 패키지로 고칠 수 있는 것만 적용한다.
set -e
export DEBIAN_FRONTEND=noninteractive
apt-get install -y -qq libpam-tmpdir libpam-pwquality apt-listchanges apt-show-versions debsums rsyslog fail2ban rkhunter >/dev/null 2>&1
# 비밀번호 정책(AUTH-9230, AUTH-9286, AUTH-9328)
sed -i 's/^#\? *UMASK.*/UMASK           027/' /etc/login.defs
sed -i 's/^PASS_MAX_DAYS.*/PASS_MAX_DAYS   90/; s/^PASS_MIN_DAYS.*/PASS_MIN_DAYS   1/' /etc/login.defs
grep -q '^SHA_CRYPT_MIN_ROUNDS' /etc/login.defs || printf 'SHA_CRYPT_MIN_ROUNDS 65536\nSHA_CRYPT_MAX_ROUNDS 65536\n' >> /etc/login.defs
# 코어 덤프 끄기(KRNL-5820)
echo '* hard core 0' >> /etc/security/limits.conf
# 접속 경고 문구(BANN-7126, BANN-7130)
# 한글 문구는 Lynis 가 WEAK 로 판정해서 영어 문구를 쓴다
printf 'Unauthorized access to this system is prohibited. Legal action may be taken against unauthorized users.\n' | tee /etc/issue /etc/issue.net >/dev/null
# 쓰지 않는 네트워크 프로토콜 모듈 막기(NETW-3200)
mkdir -p /etc/modprobe.d
for p in dccp sctp rds tipc; do echo "install $p /bin/true"; done > /etc/modprobe.d/lab-blacklist-protocols.conf
# 쓰지 않는 저장 장치 드라이버 막기(USB-1000, STRG-1846)
printf 'install usb-storage /bin/true\ninstall firewire-core /bin/true\n' > /etc/modprobe.d/lab-blacklist-storage.conf
# 파일 권한(FILE-7524)
chmod 600 /etc/crontab 2>/dev/null || true
chmod 700 /root
