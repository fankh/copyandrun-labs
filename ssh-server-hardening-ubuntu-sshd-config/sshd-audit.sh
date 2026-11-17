#!/bin/sh
# Usage: sudo sh sshd-audit.sh
# Reads the effective sshd settings with sshd -T and compares them with recommended values.
# It does not change anything.
check() {
  key=$1
  want=$2
  got=$(sshd -T | awk -v k="$key" '$1 == k { print $2; exit }')
  if [ "$got" = "$want" ]; then s=OK; else s=CHECK; fi
  printf '%-6s %-24s now=%-16s want=%s\n' "$s" "$key" "$got" "$want"
}
check permitrootlogin no
check passwordauthentication no
check permitemptypasswords no
check x11forwarding no
check maxauthtries 3
check logingracetime 30
check clientaliveinterval 300
check clientalivecountmax 2
