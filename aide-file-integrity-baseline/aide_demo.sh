#!/usr/bin/env bash
# 컨테이너에서 AIDE 로 기준선을 만들고, 파일을 바꾸고 지우고 더한 뒤 점검 결과와 종료 코드를 확인한다.
# 준비: Docker, 같은 폴더에 lab.conf, aide_gate.sh. 내 PC의 컨테이너 안에서만 실행한다.
# 실행(Git Bash): bash aide_demo.sh   (약 2분)
export MSYS_NO_PATHCONV=1
HERE="$(pwd)"; C=osk-fa-aide
docker rm -f $C >/dev/null 2>&1
docker run -d --name $C ubuntu:24.04 sleep 900 >/dev/null
docker exec $C bash -c 'apt-get update -qq >/dev/null; DEBIAN_FRONTEND=noninteractive apt-get install -y -qq aide aide-common >/dev/null 2>&1'
X() { docker exec $C sh -c "$1"; }
put() { docker exec -i $C sh -c "cat > $2" < "$1"; }
put "$HERE/lab.conf" /etc/aide/lab.conf; put "$HERE/aide_gate.sh" /usr/local/bin/aide_gate.sh; X 'chmod +x /usr/local/bin/aide_gate.sh'
echo -n "## 0. 버전: "; X 'aide --version 2>&1 | head -1'
X 'mkdir -p /srv/lab/conf /srv/lab/tmp /var/lib/aide; printf "port=8080\n" > /srv/lab/conf/app.conf; printf "user=app\n" > /srv/lab/conf/db.conf; chmod 640 /srv/lab/conf/db.conf'

echo "## 1. 기준선 만들기"
X 'aide -c /etc/aide/lab.conf --init >/dev/null 2>&1; cp /var/lib/aide/lab.db.new /var/lib/aide/lab.db; aide -c /etc/aide/lab.conf --check | grep -E "Number of entries"'
DBHASH=$(X 'sha256sum /var/lib/aide/lab.db | cut -d" " -f1')
echo "  데이터베이스 SHA-256(컨테이너 밖에 따로 적어 둠): ${DBHASH:0:16}..."

RESET='printf "port=8080\n" > /srv/lab/conf/app.conf; printf "user=app\n" > /srv/lab/conf/db.conf; chmod 640 /srv/lab/conf/db.conf; rm -f /srv/lab/conf/new.conf /srv/lab/tmp/cache.bin'
run() { echo "## $1"; X "$RESET"; X "$2"; docker exec $C aide_gate.sh; echo "  게이트 종료 코드 $?"; }
echo "## 2. 아무것도 바꾸지 않고 점검"; docker exec $C aide_gate.sh; echo "  게이트 종료 코드 $?"
run "3. 내용 한 줄 수정" 'echo "debug=true" >> /srv/lab/conf/app.conf'
run "4. 권한만 변경(640에서 666)" 'chmod 666 /srv/lab/conf/db.conf'
X "$RESET"; X 'chmod 666 /srv/lab/conf/db.conf'; docker exec $C aide_gate.sh >/dev/null; echo "## 4-1. 같은 변경의 상세 보고서(일부)"; X 'sed -n "/Detailed information/,\$p" /tmp/aide_report.txt | grep -vE "^-+$|^$" | head -3'
run "5. 파일 삭제와 새 파일 추가" 'rm /srv/lab/conf/db.conf; echo "backdoor" > /srv/lab/conf/new.conf'
run "6. 수정 시각만 바꾸고(touch) 제외한 tmp 폴더에 파일 추가" 'touch /srv/lab/conf/app.conf; echo x > /srv/lab/tmp/cache.bin'
echo "## 7. 공격자가 파일을 바꾼 뒤 기준선 DB 를 다시 만들어 흔적을 지운 경우"
X "$RESET"; X 'echo "backdoor" > /srv/lab/conf/new.conf'
X 'aide -c /etc/aide/lab.conf --init >/dev/null 2>&1; cp /var/lib/aide/lab.db.new /var/lib/aide/lab.db'
docker exec $C aide_gate.sh; echo "  게이트 종료 코드 $?  (DB 가 바뀌어 변경이 보이지 않음)"
NOW=$(X 'sha256sum /var/lib/aide/lab.db | cut -d" " -f1')
[ "$NOW" = "$DBHASH" ] && echo "  DB 해시 대조: 같음" || echo "  DB 해시 대조: 다름 -> 기준선 자체가 바뀜 (${NOW:0:16}...)"
docker rm -f $C >/dev/null
echo "## 끝"
