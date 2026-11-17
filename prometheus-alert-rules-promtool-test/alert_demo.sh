#!/usr/bin/env bash
# promtool 로 알림 규칙의 문법과 동작을 시험하고, amtool 로 라벨별 수신처(라우팅)를 시험한다. 서버는 띄우지 않는다.
# 준비: Docker (prom/prometheus:v2.51.0, prom/alertmanager:v0.27.0), 같은 폴더에 rules_good.yml, rules_bad.yml, rules_test.yml, am_good.yml, am_bad.yml.
# 실행(Git Bash): bash alert_demo.sh   (약 20초)
export MSYS_NO_PATHCONV=1
HERE="$(pwd)"
OUT=../osk-fb-prom-out                       # 작업 폴더는 이 폴더 밖에 둔다
rm -rf "$OUT"; mkdir -p "$OUT"; ABS="$(cd "$OUT" && pwd)"
PT() { docker run --rm -v "$ABS:/w" --entrypoint promtool prom/prometheus:v2.51.0 "$@"; }
AT() { docker run --rm -v "$ABS:/w" --entrypoint amtool prom/alertmanager:v0.27.0 "$@"; }
cp "$HERE/rules_test.yml" "$ABS/rules_test.yml"

echo "## 1. 문법 오류는 check rules 가 잡는다"
sed 's/> 0.05/> /' "$HERE/rules_good.yml" > "$ABS/rules.yml"
PT check rules /w/rules.yml 2>&1 | sed 's/^/  /' | cut -c1-150; echo "  종료 코드 ${PIPESTATUS[0]}"

echo "## 2. 논리 오류는 check 를 통과하고 test rules 가 잡는다"
for v in bad good; do
  cp "$HERE/rules_$v.yml" "$ABS/rules.yml"
  echo "### rules_$v.yml"
  PT check rules /w/rules.yml 2>&1 | sed 's/^/  /'
  PT test rules /w/rules_test.yml > "$ABS/test_$v.txt" 2>&1; rc=$?
  grep -E '^ +name: |SUCCESS' "$ABS/test_$v.txt" | sed 's/^ */  /; s/,$//; s/^  name:/  실패한 시험:/'
  grep -E 'alertname: [A-Za-z]+, time' "$ABS/test_$v.txt" | sed 's/^ */    어긋난 판정 /; s/, $//'
  echo "  어긋난 판정 합계 $(grep -cE 'alertname: [A-Za-z]+, time' "$ABS/test_$v.txt")건"
  echo "  test rules 종료 코드 $rc"
done

echo "## 3. Alertmanager 설정과 라우팅"
sed '/name: team-chat/,$d' "$HERE/am_good.yml" > "$ABS/am_missing.yml"
cp "$HERE/am_good.yml" "$ABS/am_good.yml"; cp "$HERE/am_bad.yml" "$ABS/am_bad.yml"
echo "### 수신처를 빠뜨린 설정"
AT check-config /w/am_missing.yml 2>&1 | grep -E 'FAILED|error|SUCCESS' | cut -c1-160 | sed 's/^/  /'
ROUTES=("severity=critical alertname=InstanceDown|pager" "severity=warning alertname=HighErrorRate|team-chat" "severity=info alertname=Other|team-default")
for v in bad good; do
  echo "### am_$v.yml 라우팅"
  AT check-config /w/am_$v.yml 2>&1 | grep -E 'SUCCESS|FAILED' | sed 's/^/  /'
  mis=0
  for r in "${ROUTES[@]}"; do
    labels="${r%%|*}"; want="${r##*|}"
    got=$(AT config routes test --config.file=/w/am_$v.yml $labels | tr -d '\r')
    mark="  "; [ "$got" != "$want" ] && { mark="X "; mis=$((mis+1)); }
    printf "  %s%-45s 기대 %-12s 실제 %s\n" "$mark" "$labels" "$want" "$got"
  done
  echo "  어긋난 칸 $mis / ${#ROUTES[@]}"
done
echo "## 4. 라우팅 트리(좋은 설정)"
AT config routes show --config.file=/w/am_good.yml | sed 's/^/  /'
echo "## 끝"
