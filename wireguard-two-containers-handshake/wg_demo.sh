#!/usr/bin/env bash
# 컨테이너 두 개 사이에 WireGuard 터널을 만들고, 정상 설정과 틀린 설정 두 가지를 같은 방법으로 점검한다.
# 준비: Docker(Linux 컨테이너, WireGuard 를 지원하는 커널), python, 같은 폴더에 wg_summary.py.
# 주의: 키는 시험용으로 매번 새로 만들며 어디에도 저장하지 않는다.
# 실행(Git Bash): bash wg_demo.sh   (약 2분)
export MSYS_NO_PATHCONV=1
NET=osk-fd-wgnet; A=osk-fd-wga; B=osk-fd-wgb
cleanup() { docker rm -f $A $B >/dev/null 2>&1; docker network rm $NET >/dev/null 2>&1; }
cleanup
docker network create $NET >/dev/null
for n in $A $B; do
  docker run -d --name $n --network $NET --cap-add NET_ADMIN alpine sh -c \
    'apk add -q wireguard-tools iproute2 tcpdump netcat-openbsd >/dev/null 2>&1 && touch /ready && sleep 3600' >/dev/null
done
for n in $A $B; do until docker exec $n test -f /ready 2>/dev/null; do sleep 1; done; done
ip_of() { docker inspect -f '{{(index .NetworkSettings.Networks "'$NET'").IPAddress}}' "$1"; }
IPA=$(ip_of $A); IPB=$(ip_of $B)
KA=$(docker exec $A wg genkey); KB=$(docker exec $B wg genkey); KX=$(docker exec $A wg genkey)
PA=$(echo "$KA" | docker exec -i $A wg pubkey); PB=$(echo "$KB" | docker exec -i $B wg pubkey); PX=$(echo "$KX" | docker exec -i $A wg pubkey)

up() {  # up <컨테이너> <개인키> <터널 IP> <상대 공개키> <상대 실제 IP> <상대에게 허용할 주소>
  docker exec -i $1 sh -c "cat > /tmp/k; ip link del wg0 2>/dev/null; ip link add wg0 type wireguard && \
    wg set wg0 listen-port 51820 private-key /tmp/k peer $4 endpoint $5:51820 allowed-ips $6 && \
    ip addr add $3/24 dev wg0 && ip link set wg0 up" <<<"$2"
}
case_run() {  # case_run <이름> <A가 믿는 B의 공개키> <A 가 B에 허용한 주소> <B 가 A에 허용한 주소>
  echo "## $1"
  up $A "$KA" 10.8.0.1 "$2" $IPB "$3"
  up $B "$KB" 10.8.0.2 "$PA" $IPA "$4"
  if docker exec $A ping -c 2 -W 2 10.8.0.2 >/dev/null 2>&1; then OK=1; else OK=0; fi
  docker exec $A wg show wg0 dump | python wg_summary.py --ping $OK; echo "  종료 코드 $?"
}
case_run "1. 정상 설정" "$PB" 10.8.0.2/32 10.8.0.1/32
case_run "2. A 가 B 의 공개키를 잘못 적음" "$PX" 10.8.0.2/32 10.8.0.1/32
case_run "3. B 가 A 의 주소를 잘못 허용함" "$PB" 10.8.0.2/32 10.9.9.9/32

echo "## 4. 겉으로 보이는 패킷에 내용이 있는가(정상 설정으로 복구해 비교)"
up $A "$KA" 10.8.0.1 "$PB" $IPB 10.8.0.2/32
up $B "$KB" 10.8.0.2 "$PA" $IPA 10.8.0.1/32
docker exec -d $B sh -c 'nc -l -p 9000 >/dev/null; true'
docker exec -d $B sh -c 'nc -l -p 9001 >/dev/null; true'
docker exec -d $A sh -c "tcpdump -nn -i eth0 -w /tmp/o.pcap host $IPB >/dev/null 2>&1"
sleep 2
docker exec $A sh -c "echo SECRETMARKER | nc -w 1 10.8.0.2 9000"      # 터널 안으로
docker exec $A sh -c "echo SECRETMARKER | nc -w 1 $IPB 9001"          # 터널 밖으로(일반 TCP)
sleep 1
docker exec $A pkill tcpdump; sleep 1
echo -n "  터널로 보낸 쪽(UDP 51820) 패킷: "; docker exec $A sh -c "tcpdump -nn -r /tmp/o.pcap udp port 51820 2>/dev/null | wc -l"
echo -n "  터널로 보낸 내용이 겉에 보인 횟수(포트 9000): "; docker exec $A sh -c "tcpdump -nn -A -r /tmp/o.pcap tcp port 9000 2>/dev/null | grep -c SECRETMARKER; true"
echo -n "  터널 밖으로 보낸 내용이 겉에 보인 횟수(포트 9001): "; docker exec $A sh -c "tcpdump -nn -A -r /tmp/o.pcap tcp port 9001 2>/dev/null | grep -c SECRETMARKER; true"
echo -n "  UDP 51820 패킷 안에 SECRETMARKER: "; docker exec $A sh -c "tcpdump -nn -A -r /tmp/o.pcap udp port 51820 2>/dev/null | grep -c SECRETMARKER; true"
echo "## 5. 겉에서 본 패킷 모양"
echo "  [터널] UDP 51820 (처음 3개)"; docker exec $A sh -c "tcpdump -nn -r /tmp/o.pcap udp port 51820 2>/dev/null | head -3 | cut -d' ' -f1-8,10-"
echo "  [터널 밖] TCP 9001 의 내용이 든 줄"; docker exec $A sh -c "tcpdump -nn -A -r /tmp/o.pcap tcp port 9001 2>/dev/null | grep SECRETMARKER | cut -c1-60"
cleanup
echo "## 끝"
