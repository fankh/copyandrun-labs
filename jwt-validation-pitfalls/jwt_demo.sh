#!/usr/bin/env bash
# 토큰 일곱 개(정상 1, 공격 6)를 서명 확인을 끈 검증기, 알고리즘을 헤더에서 읽는 검증기, 고친 검증기에 넣어 비교하고, Node 구현으로 교차 확인한다.
# 준비: Docker, 같은 폴더에 make_tokens.py, verifier_*.py, run_all.py, node_verify.js. 시험용 키는 매번 새로 만든다.
# 실행(Git Bash): bash jwt_demo.sh   (약 2분)
export MSYS_NO_PATHCONV=1
HERE="$(pwd)"
OUT=../osk-fc-jwt-out                      # 결과 폴더는 코드 폴더 밖에 둔다
rm -rf "$OUT"; mkdir -p "$OUT"; ABS="$(cd "$OUT" && pwd)"
PY() { docker run --rm -v "$HERE:/w:ro" -v "$ABS:/out" -w /w -e PYTHONPATH=/w python:3.12-slim sh -c "pip install -q pyjwt cryptography >/dev/null 2>&1; $1"; }

echo "## 1. 토큰 만들기"
PY "python make_tokens.py /out"
echo "## 2. 세 검증기 비교"
PY "python run_all.py /out nosig bad good"
echo "## 3. 검증기별 게이트"
for v in nosig bad good; do
  PY "python run_all.py /out $v >/dev/null; echo \"  verifier_$v 종료 코드 \$?\""
done
echo "## 4. 교차 확인: Node jsonwebtoken (알고리즘 고정, iss/aud 확인)"
docker run --rm -v "$HERE:/w:ro" -v "$ABS:/out:ro" -w /tmp node:22-alpine sh -c 'npm install --silent jsonwebtoken >/dev/null 2>&1; cp /w/node_verify.js /tmp/; node /tmp/node_verify.js /out; echo "  종료 코드 $?"'
echo "## 끝 (결과 폴더: $OUT)"
