#!/usr/bin/env bash
# report.md 를 Pandoc(컨테이너)으로 docx 와 html 로 바꾸고, docx 안을 확인하고, PDF 실패를 재현한다.
# 준비: Docker, 파이썬, 같은 폴더의 report.md 와 check_docx.py
# 실행: bash convert.sh
set -u
export MSYS_NO_PATHCONV=1                 # Git Bash 의 경로 변환을 끈다
HERE="$(pwd -W 2>/dev/null || pwd)"
PANDOC="docker run --rm -v $HERE:/data pandoc/core:latest"

echo "## 1. docx 와 html 변환"
$PANDOC report.md -o report.docx && ls -l report.docx | awk '{print $5, "bytes", $9}'
$PANDOC report.md -s -o report.html && echo "report.html 만들어짐"

echo "## 2. docx 안 확인"
python -X utf8 check_docx.py

echo "## 3. PDF 변환(LaTeX 가 없는 이미지라 실패하는 것이 정상)"
$PANDOC report.md -o report.pdf 2>&1 | head -2
