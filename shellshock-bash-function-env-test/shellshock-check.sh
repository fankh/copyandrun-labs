#!/bin/sh
# 사용: sh shellshock-check.sh [bash 경로]   (경로를 생략하면 PATH 의 bash)
# 환경 변수에 함수 정의와 echo 하나를 붙여 bash 를 실행한다. 출력 외에 하는 일은 없다.
# 취약한 bash 는 함수 정의 뒤의 echo 까지 실행해 VULNERABLE 을 찍는다.
B="${1:-bash}"
"$B" --version | sed -n '1p'
R=$(env x='() { :;}; echo VULNERABLE' "$B" -c 'echo test' 2>/dev/null)
case "$R" in
  *VULNERABLE*) echo "판정: 함수 정의 뒤의 명령이 실행됨 (취약)" ;;
  *) echo "판정: 함수 정의 뒤의 명령이 실행되지 않음 (패치됨)" ;;
esac
