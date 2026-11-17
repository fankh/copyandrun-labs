#!/bin/sh
# 사용: sh sudo-check.sh   (Debian, Ubuntu 계열)
# sudo 표시 버전, 패키지 버전, 패키지 변경 이력의 CVE-2021-3156 항목을 한 번에 본다.
S=$(command -v sudo) || { echo "sudo 없음: 이 서버는 영향 없음"; exit 0; }
echo "sudo 경로: $S"
echo "sudo 표시 버전: $("$S" -V | sed -n '1p')"
echo "패키지 버전: $(dpkg -s sudo | sed -n 's/^Version: //p')"
if zcat /usr/share/doc/sudo/changelog.Debian.gz | grep -q "CVE-2021-3156"; then
  echo "판정: 변경 이력에 CVE-2021-3156 수정이 있음 (패치됨)"
else
  echo "판정: 변경 이력에 CVE-2021-3156 수정이 없음 (패치 확인 필요)"
fi
