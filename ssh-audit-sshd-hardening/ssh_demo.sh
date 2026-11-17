#!/usr/bin/env bash
# 약한 sshd 와 하드닝한 sshd 를 컨테이너로 띄우고 ssh-audit 으로 비교한 뒤, 실제 ssh 클라이언트로 같은 결과를 대조한다.
# 준비: Docker, python, 같은 폴더에 sshd_weak.conf, sshd_hardened.conf, ssh_summary.py. 내 PC의 컨테이너만 점검한다.
# 실행(Git Bash): bash ssh_demo.sh   (약 2분)
export MSYS_NO_PATHCONV=1
HERE="$(pwd)"; OUT=../osk-ssh-out
rm -rf "$OUT"; mkdir -p "$OUT"
cleanup() { docker rm -f osk-fa-sshw osk-fa-sshh >/dev/null 2>&1; }
cleanup
start() {   # start <컨테이너> <설정 파일>
  docker run -d --name "$1" ubuntu:24.04 sleep 3600 >/dev/null
  docker exec "$1" bash -c 'apt-get update -qq >/dev/null; apt-get install -y -qq openssh-server openssh-client >/dev/null 2>&1; mkdir -p /run/sshd; ssh-keygen -A >/dev/null'
  docker exec -i "$1" sh -c 'cat > /etc/ssh/sshd_lab.conf' < "$2"
  docker exec "$1" /usr/sbin/sshd -t -f /etc/ssh/sshd_lab.conf || echo "  설정 오류"
  docker exec -d "$1" /usr/sbin/sshd -D -f /etc/ssh/sshd_lab.conf
}
start osk-fa-sshw "$HERE/sshd_weak.conf"
start osk-fa-sshh "$HERE/sshd_hardened.conf"
sleep 2
docker exec osk-fa-sshw sshd -V 2>&1 | head -1 | sed 's/^/## OpenSSH 서버: /'
echo "## 1. ssh-audit (약한 설정, 하드닝 설정)"
for pair in "weak osk-fa-sshw" "hardened osk-fa-sshh"; do
  set -- $pair
  docker run --rm --network container:$2 positronsecurity/ssh-audit -j --skip-rate-test 127.0.0.1 > "$OUT/$1.json" 2>/dev/null
  python ssh_summary.py "$OUT/$1.json" --list | grep -v '^      fail' ; echo "  종료 코드 ${PIPESTATUS[0]}"
done
echo "## 2. 약한 설정에서 fail 로 나온 알고리즘"
python ssh_summary.py "$OUT/weak.json" --list | grep '^      fail' | sed 's/^ *fail  *//' | tr '\n' ' ' | fold -w 100; echo

echo "## 3. 실제 ssh 클라이언트로 교차 확인(인증은 일부러 실패시키고 협상 단계만 본다)"
try() {  # try <컨테이너> <옵션>
  docker exec "$1" ssh -o BatchMode=yes -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null "${@:2}" -p 22 nobody@127.0.0.1 true 2>&1 | grep -vE 'Warning: Permanently' | head -1
}
for opt in "-o Ciphers=3des-cbc" "-o KexAlgorithms=diffie-hellman-group14-sha1" "-o Ciphers=aes256-ctr -o MACs=hmac-sha1" "-o Ciphers=aes256-gcm@openssh.com"; do
  echo "  [$opt]"
  echo -n "     약한 설정   : "; try osk-fa-sshw $opt | cut -c1-110
  echo -n "     하드닝 설정 : "; try osk-fa-sshh $opt | cut -c1-110
done
cleanup
echo "## 끝 (결과 폴더: $OUT)"
