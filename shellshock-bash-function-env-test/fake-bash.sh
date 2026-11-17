#!/bin/sh
# 취약한 bash 를 흉내 내는 시험용 스크립트다. 환경 변수 x 가 함수 정의로 시작하면 VULNERABLE 을 찍는다.
# 점검 스크립트가 취약한 경우를 판정하는지 확인하는 용도이고, 실제 bash 의 동작을 재현하지는 않는다.
case "$1" in
  --version) echo "fake bash, version 4.3.0(1)-release (emulated)"; exit 0 ;;
esac
case "$x" in
  "() {"*) echo VULNERABLE ;;
esac
echo test
