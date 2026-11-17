#!/bin/sh
# 컨테이너 안에서 AIDE 점검을 돌리고, 종료 코드를 사람이 읽는 말로 바꾼 뒤 변경이 있으면 1 로 끝낸다.
# AIDE 종료 코드는 비트 합이다: 1 추가, 2 삭제, 4 변경(8 이상은 기타 오류).
aide -c /etc/aide/lab.conf --check > /tmp/aide_report.txt 2>&1
rc=$?
if [ "$rc" -eq 0 ]; then echo "  변경 없음"; exit 0; fi
[ $((rc & 1)) -ne 0 ] && echo "  추가된 파일 있음"
[ $((rc & 2)) -ne 0 ] && echo "  삭제된 파일 있음"
[ $((rc & 4)) -ne 0 ] && echo "  변경된 파일 있음"
[ "$rc" -ge 8 ] && echo "  AIDE 오류 코드 $rc"
grep -E '^(f|d)[-+ >]' /tmp/aide_report.txt | grep ': ' | sed 's/^/    /'
exit 1
