#!/bin/sh
# SpotBugs XML 보고서에서 결과를 한 줄씩 요약합니다. 사용법: sh summary.sh target/spotbugsXml.xml
grep -oE "priority='[0-9]' type='[A-Z0-9_]+'|<Message>At [A-Za-z]+\.java:\[line [0-9]+\]" "$1" \
  | sed -E "s/priority='([0-9])' type='([A-Z0-9_]+)'/\1 \2/; s/<Message>At //" \
  | awk 'function out() { if (t != "") printf "priority=%s  %-42s %s\n", p, t, loc }
         /^[0-9] / { out(); p = $1; t = $2; loc = ""; next }
         loc == "" { loc = $0 }
         END { out() }'
