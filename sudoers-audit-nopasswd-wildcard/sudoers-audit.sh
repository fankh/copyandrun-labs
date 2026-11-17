#!/bin/sh
# Usage: sh sudoers-audit.sh [directory]   (default /etc/sudoers.d, run with sudo for the default)
# Flags risky sudoers rules: NOPASSWD, rules that allow every command, wildcards,
# editors and pagers that can open a shell, and !authenticate. It does not change anything.
dir=${1:-/etc/sudoers.d}
flag() {
  grep -nE "$2" "$f" | grep -vE '^[0-9]+:[[:space:]]*#' | while IFS= read -r l; do
    printf 'FLAG  %-10s line %s  [%s]\n' "$(basename "$f")" "$l" "$1"
  done
}
result=$(
  for f in "$dir"/*; do
    [ -f "$f" ] || continue
    flag nopasswd 'NOPASSWD'
    flag all-commands 'ALL=\([A-Za-z:]+\)[[:space:]]+(NOPASSWD:[[:space:]]*)?ALL[[:space:]]*$'
    flag wildcard '[*]'
    flag shell-escape '/(vi|vim|less|more|find|awk|man|nano)([[:space:]]|,|$)'
    flag no-authenticate '!authenticate'
  done
)
if [ -n "$result" ]; then
  printf '%s\n' "$result"
fi
count=$(printf '%s' "$result" | grep -c FLAG)
echo "flags: $count"
