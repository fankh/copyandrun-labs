#!/usr/bin/env bash
# OSV-Scanner 로 잠금 파일의 알려진 취약점을 찾고, 요약하고, 예외를 두고, 고친 뒤 다시 검사한다.
# 준비: Docker, 인터넷(api.osv.dev, deps.dev 조회). 같은 폴더에 requirements.txt, package-lock.json, osv_summary.py.
# 실행(Git Bash): bash osv_demo.sh
export MSYS_NO_PATHCONV=1   # Git Bash 가 /src 를 윈도우 경로로 바꾸지 않게 한다
IMG=ghcr.io/google/osv-scanner:latest
HERE="$(pwd)"
osv() { docker run --rm -v "$HERE:/src" "$IMG" "$@"; }

echo "## 0. 버전"
osv --version 2>&1 | head -1

echo "## 1. 폴더 전체 검사(표). 요약 줄과 종료 코드만 본다"
osv scan source -r /src > table.txt 2>&1
echo "exit code = $?"
grep -E '^Total|can be fixed' table.txt

echo "## 2. JSON 으로 받아 패키지별로 요약"
osv scan source -r --format json /src 2>/dev/null > out.json
python osv_summary.py out.json

echo "## 3. 파일 하나만 검사(-L)"
osv scan source -L /src/package-lock.json 2>&1 | grep -E '^Total|^No issues'

echo "## 4. 출력 형식별 크기(바이트)"
for f in markdown sarif cyclonedx-1-6 spdx-2-3; do
  printf '%-14s ' "$f"; osv scan source -r --format "$f" /src 2>/dev/null | wc -c
done

echo "## 5. 지적 하나에 예외(이유와 만료일 포함)를 두고 다시 검사"
cat > osv-scanner.toml <<'TOML'
[[IgnoredVulns]]
id = "GHSA-xvch-5gv4-984h"
ignoreUntil = 2027-03-31
reason = "개발 도구에서만 쓰는 minimist, 배포본에는 들어가지 않음(예시)"
TOML
osv scan source -r --config /src/osv-scanner.toml /src 2>&1 | grep -E '^Total|ignored|Ignored'
rm -f osv-scanner.toml

echo "## 6. 모든 지적을 없애는 버전으로 올린 파일을 새 폴더에 만들어 검사"
FIX="$HERE/../osv-fixed-tmp"   # 검사 대상 폴더 밖에 만든다. 안에 두면 1번 검사가 이 폴더까지 읽는다
mkdir -p "$FIX"
cat > "$FIX/requirements.txt" <<'REQ'
flask==3.1.3
jinja2==3.1.6
pyyaml==6.0.2
requests==2.33.0
urllib3==2.8.0
REQ
sed -e 's/4\.17\.15/4.18.0/g' -e 's/1\.2\.5/1.2.6/g' package-lock.json > "$FIX/package-lock.json"
docker run --rm -v "$FIX:/src" "$IMG" scan source -r /src > "$FIX/fixed.txt" 2>&1
echo "exit code = $?"
grep -E '^Total|^No issues|conflict' "$FIX/fixed.txt"

echo "## 7. 남은 둘은 직접 쓰지 않은 하위 의존성(requests 가 끌어온 것). 표에서 이름을 확인한다"
grep -E '^\| https://osv.dev/PYSEC' "$FIX/fixed.txt" | awk -F'|' '{gsub(/ +/," ",$5); gsub(/ +/," ",$6); gsub(/ +/," ",$7); print "  " $5 $6 " -> fix " $7}'

echo "## 8. 그 둘도 고정해 다시 검사"
printf 'certifi==2026.10.19\nidna==3.15\n' >> "$FIX/requirements.txt"
docker run --rm -v "$FIX:/src" "$IMG" scan source -r /src > "$FIX/fixed2.txt" 2>&1
echo "exit code = $?"
grep -E '^Total|^No issues' "$FIX/fixed2.txt"
rm -rf "$FIX" table.txt out.json
