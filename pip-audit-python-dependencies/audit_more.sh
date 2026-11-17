#!/usr/bin/env bash
# pip-audit 심화: 중복 행의 정체, 특정 취약점 제외, CycloneDX 출력, --fix 시험, 설치된 환경 점검.
# 준비: audit.sh 와 같은 폴더(requirements.txt, 가상환경 v)
# 실행: bash audit_more.sh
set -u
AUDIT=./v/Scripts/pip-audit
BASE="-r requirements.txt --no-deps --disable-pip"

echo "## 1. 같은 행이 두 번 나오는 이유: JSON 에서 (이름, ID, 별칭, 수정 버전)이 완전히 같은 항목을 센다"
$AUDIT $BASE -f json 2>/dev/null | python -X utf8 -c "
import json, sys
from collections import Counter
rows = [(d['name'], v['id'], tuple(sorted(v['aliases'])), tuple(v['fix_versions'])) for d in json.load(sys.stdin)['dependencies'] for v in d['vulns']]
c = Counter(rows)
print('행', len(rows), '/ 서로 다른 항목', len(c), '/ 두 번 이상 나온 항목', sum(1 for n in c.values() if n > 1))
"

echo "## 2. --ignore-vuln 으로 PYSEC-2018-28 제외(요약 줄)"
$AUDIT $BASE 2>&1 | grep Found
$AUDIT $BASE --ignore-vuln PYSEC-2018-28 2>&1 | grep Found

echo "## 3. CycloneDX 출력(SBOM 형식)"
$AUDIT $BASE -f cyclonedx-json 2>/dev/null | python -X utf8 -c "
import json, sys
d = json.load(sys.stdin)
print(d['bomFormat'], d['specVersion'], '구성 요소', len(d['components']), '취약점', len(d.get('vulnerabilities', [])))
"

echo "## 4. --fix --dry-run (--no-deps 와 함께 쓰면 어떻게 되나)"
$AUDIT $BASE --fix --dry-run 2>&1 | grep 'Dry run'
echo "종료 코드: ${PIPESTATUS[0]}"

echo "## 5. 지금 가상환경에 설치된 패키지 점검(-r 없이)"
$AUDIT 2>&1 | tail -3
