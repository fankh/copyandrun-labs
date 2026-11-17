#!/bin/sh
# 시험용 nginx 를 띄우고 요청 10번으로 access 로그를 만든 뒤 access.log 로 복사합니다.
# Referer 와 X-Forwarded-For 는 직접 써 넣은 가짜 값이며 어디에도 접속하지 않습니다.
docker build -q -t cr-fx-nginx:latest . >/dev/null && echo built
docker rm -f cr-fx-web >/dev/null 2>&1
docker run -d --name cr-fx-web -p 127.0.0.1:18272:80 cr-fx-nginx:latest >/dev/null
sleep 2

req() {  # req <xff> <referer> <경로>
  curl -s -o /dev/null -A lab-test/1.0 -H "X-Forwarded-For: $1" -e "$2" "http://127.0.0.1:18272$3"
}
req 10.20.0.5 ""                                          /
req 10.20.0.5 "http://www.example.com/"                   /index.html
req 10.20.0.6 "http://evil.example.net/landing"           /
req 10.20.0.6 "http://cdn.evil.example.net/x"             /
req 10.20.0.8 "http://notevil.example.net/"               /
req 10.20.0.7 ""                                          /
req 10.20.0.70 ""                                         /
req 10.20.0.9 "http://files.example.org/u/111/setup.exe"  /
req 10.20.0.9 "http://files.example.org/u/999/logo.png"   /
req 10.20.0.4 "http://cdn.example.com/lib.js"             /

MSYS_NO_PATHCONV=1 docker exec cr-fx-web cat /var/log/nginx/lab_access.log > access.log
wc -l access.log
