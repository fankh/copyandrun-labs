#!/bin/sh
# 사용: sh xz-check.sh [xz 버전]   (버전을 생략하면 xz --version 의 값)
# CVE-2024-3094: 백도어가 들어 있던 릴리스는 5.6.0 과 5.6.1 이다.
# 설치된 xz 버전과, sshd 가 liblzma 를 불러오는지(ldd)를 함께 본다. 읽기만 한다.
V="${1:-$(xz --version 2>/dev/null | sed -n '1s/.* //p')}"
[ -n "$V" ] || { echo "xz 없음: 이 서버는 xz 를 쓰지 않음"; exit 0; }
echo "xz 버전: $V"
case "$V" in
  5.6.0|5.6.1) echo "판정: 백도어가 들어 있던 릴리스 (5.6.0, 5.6.1)" ;;
  *) echo "판정: 5.6.0, 5.6.1 이 아님" ;;
esac
SSHD=$(command -v sshd) || { echo "sshd 없음"; exit 0; }
N=$(ldd "$SSHD" | grep -c lzma)
echo "sshd 가 불러오는 liblzma 항목: $N개"
