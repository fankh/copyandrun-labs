#!/usr/bin/env bash
# requirements.txt 의 파이썬 의존성을 pip-audit 로 점검하고 고유 취약점 수를 센다.
# 준비: python -m venv v && ./v/Scripts/python -m pip install pip-audit   (Linux는 ./v/bin/)
# 실행: bash audit.sh
set -u
AUDIT=./v/Scripts/pip-audit

echo "## 1. 점검(취약한 버전 3개)"
$AUDIT -r requirements.txt --no-deps --disable-pip 2>/dev/null
echo "종료 코드: $?"

echo "## 2. JSON 으로 받아 패키지별 고유 취약점 세기"
$AUDIT -r requirements.txt --no-deps --disable-pip -f json 2>/dev/null | python -X utf8 -c "
import json, sys
for d in json.load(sys.stdin)['dependencies']:
    ids = {v['id'] for v in d['vulns']}
    fixes = sorted({f for v in d['vulns'] for f in v['fix_versions']})
    print(d['name'], d['version'], '행', len(d['vulns']), '고유 ID', len(ids), '가장 높은 수정 버전', fixes[-1] if fixes else '-')
"

echo "## 3. 고친 버전 파일(requests==2.33.0)"
printf 'requests==2.33.0\n' > clean.txt
$AUDIT -r clean.txt --no-deps --disable-pip 2>&1 | grep -v WARNING
echo "종료 코드: ${PIPESTATUS[0]}"
