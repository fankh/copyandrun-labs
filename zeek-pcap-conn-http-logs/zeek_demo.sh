#!/usr/bin/env bash
# 내 PC의 웹 컨테이너 트래픽을 pcap 으로 저장하고, Zeek 가 그 파일을 읽어 conn.log 와 http.log 를 만드는지 확인한다.
# 준비: Docker, python, 같은 폴더에 nginx_lab.conf, zeek_summary.py.
# 실행(Git Bash): bash zeek_demo.sh   (약 2분)
export MSYS_NO_PATHCONV=1
HERE="$(pwd)"
OUT=../osk-fd-zeek-out                  # 결과 폴더는 스크립트 폴더 밖에 둔다. Windows 의 python 이 읽도록 상대 경로로 둔다
rm -rf "$OUT"; mkdir -p "$OUT"; ABS="$(cd "$OUT" && pwd)"
cleanup() { docker rm -f osk-fd-zweb osk-fd-zsniff >/dev/null 2>&1; docker network rm osk-fd-znet >/dev/null 2>&1; }
cleanup
docker network create osk-fd-znet >/dev/null
docker run -d --name osk-fd-zweb --network osk-fd-znet -v "$HERE/nginx_lab.conf:/etc/nginx/conf.d/default.conf:ro" nginx:alpine >/dev/null
sleep 2

capture() {   # capture <이름> <함수> : tcpdump 를 켜고, 그 사이에 트래픽을 만든 뒤 pcap 으로 저장
  local name="$1"; shift
  docker run -d --name osk-fd-zsniff --network container:osk-fd-zweb --cap-add NET_RAW --cap-add NET_ADMIN \
    -v "$ABS:/out" nicolaka/netshoot tcpdump -i eth0 -U -w "/out/$name.pcap" >/dev/null
  sleep 2
  "$@"
  sleep 1
  docker stop osk-fd-zsniff >/dev/null; docker rm osk-fd-zsniff >/dev/null
}
C() { docker run --rm --network osk-fd-znet curlimages/curl -s -o /dev/null "$@"; }
clean_traffic() {
  for p in / /health /login; do C "http://osk-fd-zweb$p"; done
}
scan_traffic() {
  for p in /admin /.env /backup.zip /wp-login.php /phpmyadmin /config.php /.git/config /server-status; do
    C -A 'sqlmap/1.7' "http://osk-fd-zweb$p"
  done
  C -A 'sqlmap/1.7' -d 'user=admin&pw=1' http://osk-fd-zweb/login
}
echo "## 1. pcap 만들기"
capture clean clean_traffic
capture scan scan_traffic
for n in clean scan; do
  T=$(docker run --rm -v "$ABS:/out" --entrypoint sh nicolaka/netshoot -c "tcpdump -nn -r /out/$n.pcap tcp 2>/dev/null | wc -l")
  O=$(docker run --rm -v "$ABS:/out" --entrypoint sh nicolaka/netshoot -c "tcpdump -nn -r /out/$n.pcap 'not tcp' 2>/dev/null | wc -l")
  echo "$T" > "$OUT/$n.pkts"; echo "  $n.pcap: TCP 패킷 $T개, 그 밖의 패킷(ARP) $O개"
done

for n in clean scan; do
  mkdir -p "$OUT/log-$n"
  docker run --rm -v "$ABS:/out" -w "/out/log-$n" zeek/zeek:latest zeek -C -r "/out/$n.pcap" LogAscii::use_json=T >/dev/null 2>&1
  for f in conn http; do mv "$OUT/log-$n/$f.log" "$OUT/log-$n/$f.json" 2>/dev/null; done
done
echo "## 2. 정상 pcap의 Zeek 로그"
python zeek_summary.py "$OUT/log-clean" --pcap-packets "$(cat "$OUT/clean.pkts")"; echo "  종료 코드 $?"
echo "## 3. 스캔 pcap의 Zeek 로그"
python zeek_summary.py "$OUT/log-scan" --pcap-packets "$(cat "$OUT/scan.pkts")"; echo "  종료 코드 $?"
cleanup
echo "## 끝 (결과 폴더: $OUT)"
