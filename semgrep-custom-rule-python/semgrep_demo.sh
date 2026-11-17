#!/usr/bin/env bash
# 내가 만든 semgrep 규칙 여섯 개를 시험하고, 약한 코드와 고친 코드에 적용하고, bandit 과 비교하고, 규칙을 일부러 깨 본다.
# 준비: Docker, python, 같은 폴더에 company.yml, company.py, bad_app.py, good_app.py, semgrep_summary.py. 이미지는 처음 받을 때 몇 분 걸린다.
# 실행(Git Bash): bash semgrep_demo.sh   (약 3분)
export MSYS_NO_PATHCONV=1
HERE="$(pwd)"
OUT=../osk-fc-sg-out                       # 결과 폴더는 규칙 폴더 밖에 둔다
rm -rf "$OUT"; mkdir -p "$OUT"; ABS="$(cd "$OUT" && pwd)"
SG() { docker run --rm -v "$HERE:/src:ro" -v "$ABS:/out" -w /src semgrep/semgrep semgrep "$@"; }

echo "## 1. 규칙 시험(semgrep --test)"
SG --test . 2>&1 | grep -E '[0-9]+/[0-9]+'

echo "## 2. 약한 코드와 고친 코드에 적용"
for f in bad_app good_app; do
  SG scan --config company.yml --metrics off --quiet --json -o /out/$f.json $f.py >/dev/null 2>&1
  echo "[$f.py]"; python semgrep_summary.py "$OUT/$f.json"; echo "  종료 코드 $?"
done

echo "## 3. 교차 확인: bandit 이 같은 파일에서 찾는 것"
docker run --rm -v "$HERE:/code:ro" python:3.12-alpine sh -c 'pip install -q bandit >/dev/null 2>&1; bandit /code/bad_app.py /code/good_app.py -f custom --msg-template "{relpath}:{line} {test_id} {msg}" 2>/dev/null'   | grep '^code/' | sed 's#^code/##' | cut -c1-88 > "$OUT/bandit.txt"
for f in bad_app good_app; do echo "  $f.py: bandit $(grep -c "^$f.py" "$OUT/bandit.txt")건"; done
grep '^good_app' "$OUT/bandit.txt" | sed 's/^/    /'

echo "## 4. 규칙을 일부러 깨 보기: 정리(sanitizer) 항목 삭제"
mkdir -p "$OUT/broken"; cp company.py "$OUT/broken/"
python - "$OUT" <<'PY'
import sys
s = open("company.yml", encoding="utf-8").read()
cut = s.index("    pattern-sanitizers:")
end = s.index("  - id: company-subprocess-shell-true")
open(sys.argv[1] + "/broken/company.yml", "w", encoding="utf-8", newline="\n").write(s[:cut] + "\n" + s[end:])
PY
docker run --rm -v "$ABS/broken:/b:ro" -w /b semgrep/semgrep semgrep --test . 2>&1 | grep -E '✓|✘|[0-9]+/[0-9]+|company-os' | head -6
echo "## 끝 (결과 폴더: $OUT)"
