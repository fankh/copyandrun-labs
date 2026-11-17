#!/bin/sh
# 사용: sh pwnkit-check.sh   (Debian, Ubuntu 계열)
# pkexec 버전 표시, 패키지 버전, SUID 비트, 패키지 변경 이력의 CVE-2021-4034 항목을 한 번에 본다.
P=$(command -v pkexec) || { echo "pkexec 없음: 이 서버는 영향 없음"; exit 0; }
echo "pkexec 경로: $P"
echo "pkexec 표시 버전: $("$P" --version)"
echo "패키지 버전: $(dpkg -s policykit-1 | sed -n 's/^Version: //p')"
echo "SUID 비트: $(ls -l "$P" | cut -c1-10)"
if zcat /usr/share/doc/policykit-1/changelog.Debian.gz | grep -q "CVE-2021-4034"; then
  echo "판정: 변경 이력에 CVE-2021-4034 수정이 있음 (패치됨)"
else
  echo "판정: 변경 이력에 CVE-2021-4034 수정이 없음 (패치 확인 필요)"
fi
