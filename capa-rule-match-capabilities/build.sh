#!/bin/sh
# 시험 프로그램 세 개를 윈도우 실행 파일(PE)로 컴파일한다. 실행하지 않는다.
set -e
CC=x86_64-w64-mingw32-gcc
mkdir -p out
$CC -O0 -o out/empty.exe empty.c
$CC -O0 -o out/fileio.exe fileio.c
$CC -O0 -o out/sockdemo.exe sockdemo.c -lws2_32
ls -l out
