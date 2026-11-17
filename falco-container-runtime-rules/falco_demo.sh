#!/usr/bin/env bash
# Falco 에 사용자 규칙 세 개를 주고, 평범한 컨테이너와 수상한 동작을 한 컨테이너에서 같은 방법으로 점검한다.
# 준비: Docker Desktop(WSL2), python, 같은 폴더에 lab_rules.yaml, falco_summary.py.
# 주의: Falco 는 --privileged 와 docker.sock 이 필요한 도구라 내 PC 시험 환경에서만 실행한다.
# 실행(Git Bash): bash falco_demo.sh   (약 2분)
export MSYS_NO_PATHCONV=1
HERE="$(pwd)"
OUT=../osk-fd-falco-out
rm -rf "$OUT"; mkdir -p "$OUT"
cleanup() { docker rm -f osk-fd-falco osk-fd-fclean osk-fd-fatk osk-fd-fcanary >/dev/null 2>&1; }
cleanup
docker run -d --name osk-fd-fclean alpine sleep 3600 >/dev/null
docker run -d --name osk-fd-fatk alpine sleep 3600 >/dev/null
docker run -d --name osk-fd-fcanary alpine sleep 3600 >/dev/null

echo "## 1. Falco 시작(modern eBPF 드라이버, 규칙은 기본 규칙 + 내 규칙)"
docker run -d --name osk-fd-falco --privileged \
  -v /var/run/docker.sock:/host/var/run/docker.sock -v /proc:/host/proc:ro \
  -v "$HERE/lab_rules.yaml:/etc/falco/lab_rules.yaml:ro" \
  falcosecurity/falco:latest falco -o engine.kind=modern_ebpf -o json_output=true \
  -o json_include_output_properties=true -o rule_matching=all -r /etc/falco/falco_rules.yaml -r /etc/falco/lab_rules.yaml >/dev/null
# 로그에 "Opening" 줄이 보여도 컨테이너 정보가 준비되기 전일 수 있어서, 카나리아 컨테이너의 이벤트가 잡힐 때까지 기다린다
until docker logs osk-fd-falco 2>&1 | grep -q "Opening 'syscall' source with modern BPF probe"; do sleep 1; done
n=0; until docker logs osk-fd-falco 2>&1 | grep -q 'container=osk-fd-fcanary'; do docker exec osk-fd-fcanary sh -c true; sleep 2; n=$((n+1)); [ $n -gt 40 ] && { echo "Falco 준비 실패"; cleanup; exit 1; }; done
docker logs osk-fd-falco 2>&1 | grep -E 'Falco version|System info' | sed 's/^[^ ]* //' | cut -c1-100

echo "## 2. 평범한 동작(clean 컨테이너)과 수상한 동작(atk 컨테이너)"
docker exec osk-fd-fclean ls /tmp >/dev/null
docker exec osk-fd-fclean cat /etc/hostname >/dev/null
echo "  clean: ls /tmp, cat /etc/hostname"
docker exec osk-fd-fatk sh -c 'echo test > /etc/lab_marker; cat /etc/shadow >/dev/null'
echo "  atk  : sh -c 'echo test > /etc/lab_marker; cat /etc/shadow'"
sleep 4
docker logs osk-fd-falco > "$OUT/falco.log" 2>&1

echo "## 3. 컨테이너별 LAB 규칙 건수"
python falco_summary.py "$OUT/falco.log" osk-fd-fclean; echo "    종료 코드 $?"
python falco_summary.py "$OUT/falco.log" osk-fd-fatk;   echo "    종료 코드 $?"
echo "## 4. LAB 이 아닌 기본 규칙이 같은 동작에서 낸 경고"
python - "$OUT/falco.log" <<'PY'
import json, sys
sys.stdout.reconfigure(encoding="utf-8")
seen = {}
for line in open(sys.argv[1], encoding="utf-8", errors="replace"):
    if not line.startswith("{"):
        continue
    e = json.loads(line)
    c = e.get("output_fields", {}).get("container.name", "")
    if c in ("osk-fd-fclean", "osk-fd-fatk") and not e["rule"].startswith("LAB"):
        seen[(c, e["rule"], e["priority"])] = seen.get((c, e["rule"], e["priority"]), 0) + 1
for (c, r, p), n in sorted(seen.items()):
    print(f"  {c}  {n}건  [{p}] {r}")
if not seen:
    print("  없음")
PY
cleanup
echo "## 끝 (로그: $OUT/falco.log)"
