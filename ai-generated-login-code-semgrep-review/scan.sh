#!/bin/sh
# 사용법: sh scan.sh 파일...   (Semgrep 공식 이미지로 레지스트리 규칙과 직접 쓴 규칙을 함께 적용)
# Git Bash 에서 -w /src 의 경로가 바뀌지 않게 합니다.
export MSYS_NO_PATHCONV=1
docker run --rm -v "$(pwd -W 2>/dev/null || pwd):/src" -w /src semgrep/semgrep:latest \
  semgrep scan --config p/python --config p/flask --config login-extra.yml \
  --metrics off --disable-version-check --json --quiet "$@" > result.json
python -X utf8 summarize.py result.json
