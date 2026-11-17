#!/bin/sh
# 컨테이너 안에서 시험 파일을 컴파일하고 버전을 확인한다. 만든 파일은 실행하지 않는다.
set -e
x86_64-w64-mingw32-gcc -O0 -o demo.exe demo.c
file demo.exe
ls -l demo.exe
