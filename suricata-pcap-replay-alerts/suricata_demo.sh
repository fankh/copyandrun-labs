#!/usr/bin/env bash
# 내 PC의 웹 컨테이너 트래픽을 pcap 으로 저장하고, Suricata 가 그 파일을 읽어(replay) 사용자 규칙으로 alert 를 내는지 확인한다.
# 준비: Docker, 같은 폴더에 local.rules, nginx_lab.conf, suricata_summary.py, python.
# 실행(Git Bash): bash suricata_demo.sh   (약 2분)
export MSYS_NO_PATHCONV=1
HERE="$(pwd)"
OUT=../osk-suricata-out                 # 결과 폴더는 규칙 폴더 밖에 둔다. Windows 의 python 이 읽도록 상대 경로로 둔다
rm -rf "$OUT"; mkdir -p "$OUT"; ABS="$(cd "$OUT" && pwd)"
cleanup() { docker rm -f osk-web osk-sniff >/dev/null 2>&1; docker network rm osk-net >/dev/null 2>&1; }
cleanup
docker network create osk-net >/dev/null
docker run -d --name osk-web --network osk-net -v "$HERE/nginx_lab.conf:/etc/nginx/conf.d/default.conf:ro" nginx:alpine >/dev/null
sleep 2

capture() {   # capture <이름> <명령...> : tcpdump 를 켜고, 그 사이에 트래픽을 만든 뒤 pcap 으로 저장
  local name="$1"; shift
  docker run -d --name osk-sniff --network container:osk-web --cap-add NET_RAW --cap-add NET_ADMIN \
    -v "$ABS:/out" nicolaka/netshoot tcpdump -i eth0 -U -w "/out/$name.pcap" >/dev/null
  sleep 2
  "$@"
  sleep 1
  docker stop osk-sniff >/dev/null; docker rm osk-sniff >/dev/null
}
clean_traffic() {
  for p in / /health /index.html; do docker run --rm --network osk-net curlimages/curl -s -o /dev/null "http://osk-web$p"; done
}
attack_traffic() {
  docker run --rm --network osk-net instrumentisto/nmap -p 1-100 -T4 osk-web >/dev/null
  docker run --rm --network osk-net curlimages/curl -s -o /dev/null -d 'user=admin&password=passw0rd' http://osk-web/login
  docker run --rm --network osk-net curlimages/curl -s -o /dev/null --path-as-is 'http://osk-web/../../etc/passwd'
}
echo "## 1. pcap 만들기"
capture clean clean_traffic
capture attack attack_traffic
ls -l "$OUT"/*.pcap | awk '{print "  " $5 " 바이트  " $9}' | sed "s#$OUT/##"

replay() {    # replay <이름> : Suricata 가 pcap 을 읽고 eve.json 을 남긴다
  mkdir -p "$OUT/log-$1"
  docker run --rm -v "$HERE:/rules:ro" -v "$ABS:/out" --entrypoint suricata jasonish/suricata:latest \
    -r "/out/$1.pcap" -S /rules/local.rules -l "/out/log-$1" -k none >"$OUT/run-$1.txt" 2>&1
}
echo "## 2. 정상 pcap 재생"
replay clean
python suricata_summary.py "$OUT/log-clean/eve.json"; echo "  종료 코드 $?"
echo "## 3. 공격 pcap 재생"
replay attack
python suricata_summary.py "$OUT/log-attack/eve.json"; echo "  종료 코드 $?"
echo "## 4. 같은 eve.json 의 http 이벤트(요청 줄과 응답 코드)"
python - "$OUT/log-attack/eve.json" <<'PY'
import json, sys
sys.stdout.reconfigure(encoding="utf-8")
for line in open(sys.argv[1], encoding="utf-8"):
    e = json.loads(line)
    if e["event_type"] == "http":
        h = e["http"]
        print(f"  {h.get('http_method')} {h.get('url')} -> {h.get('status')}")
PY
cleanup
echo "## 끝 (결과 폴더: $OUT)"
