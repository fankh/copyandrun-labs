#!/usr/bin/env bash
# sshd 가 도는 컨테이너에 fail2ban 을 올리고, 다른 컨테이너에서 비밀번호를 틀려 차단되는지, 차단이 풀리는지 확인한다.
# 준비: Docker, 같은 폴더에 jail.local. 내 PC의 컨테이너끼리만 접속한다(서버에만 NET_ADMIN 권한을 준다).
# 실행(Git Bash): bash f2b_demo.sh   (약 3분)
export MSYS_NO_PATHCONV=1
HERE="$(pwd)"; PW='Correct-Horse-9'
cleanup() { docker rm -f osk-fa-f2b osk-fa-atk osk-fa-ok >/dev/null 2>&1; docker network rm osk-fa-f2b-net >/dev/null 2>&1; }
cleanup; FAIL=0
docker network create osk-fa-f2b-net >/dev/null
docker run -d --name osk-fa-f2b --network osk-fa-f2b-net --network-alias srv.lab --cap-add NET_ADMIN --cap-add NET_RAW ubuntu:24.04 sleep 3600 >/dev/null
for c in osk-fa-atk osk-fa-ok; do docker run -d --name $c --network osk-fa-f2b-net ubuntu:24.04 sleep 3600 >/dev/null; done
docker exec osk-fa-f2b bash -c 'apt-get update -qq >/dev/null; DEBIAN_FRONTEND=noninteractive apt-get install -y -qq openssh-server fail2ban iptables rsyslog >/dev/null 2>&1
  mkdir -p /run/sshd; ssh-keygen -A >/dev/null; useradd -m labuser; echo "labuser:'$PW'" | chpasswd
  sed -i "s/^module(load=\"imklog\".*/#&/" /etc/rsyslog.conf     # 컨테이너에서는 커널 로그를 못 읽는다
  touch /var/log/auth.log; chown syslog:adm /var/log/auth.log'
for c in osk-fa-atk osk-fa-ok; do docker exec $c bash -c 'apt-get update -qq >/dev/null; apt-get install -y -qq openssh-client sshpass >/dev/null 2>&1'; done
docker exec -i osk-fa-f2b sh -c 'cat > /etc/fail2ban/jail.local' < "$HERE/jail.local"
docker exec -d osk-fa-f2b rsyslogd -n; sleep 2           # sshd 보다 먼저 떠야 로그가 남는다
docker exec -d osk-fa-f2b /usr/sbin/sshd -D; sleep 1
docker exec osk-fa-f2b fail2ban-client -x start >/dev/null 2>&1; sleep 3
echo -n "## 0. 버전: "; docker exec osk-fa-f2b fail2ban-client --version | head -1
login() { docker exec "$1" sshpass -p "$2" ssh -o StrictHostKeyChecking=no -o ConnectTimeout=4 labuser@srv.lab "echo 로그인성공" 2>&1 | tail -1; }
jail() { docker exec osk-fa-f2b fail2ban-client status sshd | grep -E 'Currently banned|Total failed|Banned IP' | sed 's/^[ |`-]*/    /'; }
expect() { [ "$2" = "$3" ] || { echo "    ^ 기대와 다름: $2"; FAIL=1; }; }   # expect <설명> <기대 포함 문구> <실제>

echo "## 1. 차단 전: 공격 컨테이너가 비밀번호를 3번 틀림"
for i in 1 2 3; do echo -n "  시도 $i: "; login osk-fa-atk wrong; done
sleep 3; jail
echo "## 2. 차단 후: 4번째 시도와 올바른 비밀번호"
r=$(login osk-fa-atk wrong);   echo "  틀린 비밀번호: $r";   case "$r" in *refused*) ;; *) FAIL=1;; esac
r=$(login osk-fa-atk "$PW");   echo "  올바른 비밀번호: $r"; case "$r" in *refused*) ;; *) FAIL=1;; esac
r=$(login osk-fa-ok "$PW");    echo "  다른 컨테이너(올바른 비밀번호): $r"; case "$r" in *로그인성공*) ;; *) FAIL=1;; esac
echo "  서버의 iptables:"; docker exec osk-fa-f2b iptables -S f2b-sshd | sed 's/^/    /'
echo "  fail2ban 로그:"; docker exec osk-fa-f2b grep -E 'Found|Ban ' /var/log/fail2ban.log | sed 's/^[0-9-]* //' | cut -c1-90 | tail -4 | sed 's/^/    /'

echo "## 3. 수동 해제"
docker exec osk-fa-f2b fail2ban-client set sshd unbanip $(docker exec osk-fa-f2b fail2ban-client status sshd | sed -n 's/.*Banned IP list:[ \t]*//p') >/dev/null
r=$(login osk-fa-atk "$PW"); echo "  해제 직후 올바른 비밀번호: $r"; case "$r" in *로그인성공*) ;; *) FAIL=1;; esac

echo "## 4. 다시 차단하고 시간이 지나 자동으로 풀리는지(bantime 40초)"
for i in 1 2 3; do login osk-fa-atk wrong >/dev/null; done; sleep 2
r=$(login osk-fa-atk "$PW"); echo "  차단 직후: $r"
T0=$(date +%s)
until [ "$(login osk-fa-atk "$PW")" = "로그인성공" ]; do sleep 2; [ $(( $(date +%s) - T0 )) -gt 90 ] && { echo "  90초 안에 풀리지 않음"; FAIL=1; break; }; done
echo "  자동 해제까지 약 $(( $(date +%s) - T0 ))초"
cleanup
echo "## 게이트 종료 코드: $FAIL"
exit $FAIL
