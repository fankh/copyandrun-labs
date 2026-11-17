#!/bin/sh
# Usage: sh account-audit.sh [passwd_file] [shadow_file]
# Defaults: /etc/passwd and /etc/shadow (reading shadow needs sudo). It does not change anything.
# Flags: extra UID 0 accounts, system accounts with a login shell, duplicate UIDs, empty passwords.
passwd=${1:-/etc/passwd}
shadow=${2:-/etc/shadow}
result=$(
  awk -F: '$3 == 0 && $1 != "root" { printf "FLAG  uid0         %s has UID 0\n", $1 }' "$passwd"
  awk -F: '$3 > 0 && $3 < 1000 && $7 !~ /(nologin|false)$/ { printf "FLAG  system-shell %s (uid %s) has shell %s\n", $1, $3, $7 }' "$passwd"
  awk -F: '{ n[$3]++; u[$3] = u[$3] " " $1 } END { for (i in n) if (n[i] > 1) printf "FLAG  duplicate-uid uid %s is used by:%s\n", i, u[i] }' "$passwd"
  if [ -r "$shadow" ]; then
    awk -F: '$2 == "" { printf "FLAG  empty-password %s has an empty password\n", $1 }' "$shadow"
  else
    echo "NOTE  shadow file is not readable, run with sudo to check passwords"
  fi
)
if [ -n "$result" ]; then
  printf '%s\n' "$result"
fi
count=$(printf '%s\n' "$result" | grep -c '^FLAG')
echo "flags: $count"
