#!/usr/bin/env bash
# 새 우분투 컨테이너를 Lynis 로 점검하고, 보완 스크립트를 적용한 뒤 다시 점검해 점수와 제안을 비교한다.
# 준비: Docker, python, 같은 폴더에 lynis_fix.sh, lynis_summary.py. 내 PC의 컨테이너만 점검한다.
# 실행(Git Bash): bash lynis_demo.sh   (약 3분)
export MSYS_NO_PATHCONV=1
OUT=../osk-lynis-out                   # 결과 폴더는 스크립트 폴더 밖에 둔다
rm -rf "$OUT"; mkdir -p "$OUT"
docker rm -f osk-fa-lynis >/dev/null 2>&1
docker run -d --name osk-fa-lynis ubuntu:24.04 sleep 3600 >/dev/null
docker exec osk-fa-lynis bash -c 'apt-get update -qq >/dev/null && apt-get install -y -qq lynis >/dev/null 2>&1'
echo -n "## 0. Lynis 버전: "; docker exec osk-fa-lynis lynis --version
audit() { docker exec osk-fa-lynis bash -c 'lynis audit system --quick --no-colors >/dev/null 2>&1'
          docker exec osk-fa-lynis cat /var/log/lynis-report.dat > "$OUT/$1.dat"; }

echo "## 1. 보완 전 점검"
audit before
python lynis_summary.py "$OUT/before.dat" --ignore LOGG-2138; echo "  종료 코드 $?"

echo "## 2. 보완 스크립트 적용"
docker exec -i osk-fa-lynis sh < lynis_fix.sh && echo "  적용 완료"

echo "## 3. 보완 후 점검"
audit after
python lynis_summary.py "$OUT/after.dat" --ignore LOGG-2138 --diff "$OUT/before.dat"; echo "  종료 코드 $?"
docker rm -f osk-fa-lynis >/dev/null
echo "## 끝 (결과 폴더: $OUT)"
