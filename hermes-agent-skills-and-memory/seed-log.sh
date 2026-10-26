#!/bin/bash
# 연습용 로그 파일을 만듭니다. 컨테이너 안에서만 실행합니다.
cat > "$HOME/practice/app.log" <<LOG
2026-10-24 09:00:01 INFO service started
2026-10-24 09:00:05 ERROR db connection refused
2026-10-24 09:01:12 WARN slow query 1200ms
2026-10-24 09:02:30 ERROR timeout calling payment
2026-10-24 09:03:44 INFO request ok
2026-10-24 09:04:10 ERROR db connection refused
LOG
wc -l "$HOME/practice/app.log"
