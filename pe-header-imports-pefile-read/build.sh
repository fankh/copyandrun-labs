#!/bin/sh
# 윈도우 64비트 실행 파일(PE)로 컴파일만 합니다. 만든 파일은 실행하지 않습니다.
x86_64-w64-mingw32-gcc sample.c -o sample.exe -lwininet -s
ls -l sample.exe
