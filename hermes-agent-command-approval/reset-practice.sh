#!/bin/bash
# 연습용 폴더를 처음 상태로 되돌립니다. 컨테이너 안에서만 실행합니다.
set -e
P="$HOME/practice"
rm -rf "$P/old-notes" "$P/temp-b"
mkdir -p "$P/old-notes"
echo hello > "$P/memo.txt"
echo a > "$P/old-notes/a.txt"
echo b > "$P/old-notes/b.txt"
ls -R "$P"
