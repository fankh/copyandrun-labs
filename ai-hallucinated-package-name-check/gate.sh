#!/bin/sh
# 설치 전에 이름부터 점검합니다. 점검이 실패하면 pip install 은 실행되지 않습니다.
set -e
python pkgcheck.py requirements.txt "$@"
echo "이름 점검 통과, 설치를 진행합니다"
pip install -r requirements.txt
