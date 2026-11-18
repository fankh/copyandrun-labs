#!/bin/sh
# 사용: sh java-inventory.sh [-o 결과.csv] [-n] [-f 컨테이너이름] [찾을 폴더 ...]
#   찾을 폴더를 생략하면 / 전체를 찾는다.
#   -o  결과 CSV 파일 (기본: java-inventory-<호스트>.csv)
#   -n  컨테이너 안은 보지 않는다
#   -f  이름에 이 글자가 든 컨테이너만 본다
# 서버에 있는 Java 런타임을 모두 찾아 공급업체, 전체 빌드 버전, 아키텍처, 실행 중인 프로세스를 CSV 로 남긴다.
#   1) 디스크의 bin/java 파일 (제품에 함께 설치된 런타임 포함)
#   2) 실행 중인 java 프로세스가 쓰는 런타임
#   3) 실행 중인 도커 컨테이너 안의 bin/java
# 찾은 java 를 -version 으로 한 번씩 실행해 버전을 읽는다. 그 밖에는 읽기만 한다.
# 모든 프로세스와 폴더를 보려면 root 로 실행한다.
OUT=""; NOCT=0; CTF=""
while getopts "o:nf:" o; do
  case "$o" in
    o) OUT="$OPTARG" ;;
    n) NOCT=1 ;;
    f) CTF="$OPTARG" ;;
    *) echo "사용: sh java-inventory.sh [-o 결과.csv] [-n] [-f 컨테이너이름] [찾을 폴더 ...]"; exit 2 ;;
  esac
done
shift $((OPTIND - 1))
[ $# -gt 0 ] || set -- /
HOST="$(hostname 2>/dev/null || uname -n)"
OUT="${OUT:-java-inventory-$HOST.csv}"
OSNAME="$( (. /etc/os-release 2>/dev/null && echo "$PRETTY_NAME") )"
[ -n "$OSNAME" ] || OSNAME="$(uname -sr)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

# probe: 표준 입력으로 받은 java 경로마다 "경로|공급업체|버전|런타임 빌드|아키텍처" 한 줄을 낸다.
# 컨테이너 안에서도 같은 코드를 쓰기 위해 문자열로 둔다.
PROBE='while IFS= read -r j; do
  p="$("$j" -XshowSettings:properties -version 2>&1)"
  g() { echo "$p" | sed -n "s/^ *$1 = //p" | head -1; }
  v="$(g java.version)"
  [ -n "$v" ] || v="$(echo "$p" | head -1)"
  echo "$j|$(g java.vendor)|$v|$(g java.runtime.version)|$(g os.arch)"
done'

# 1) 디스크에서 찾기. 가상 파일 시스템과 컨테이너 저장소는 건너뛴다(컨테이너는 3번에서 본다).
find "$@" \( -path /proc -o -path /sys -o -path /dev -o -path /run -o -path /var/lib/docker -o -path /var/lib/containerd -o -path /var/lib/containers \) -prune \
  -o \( -type f -o -type l \) -name java -path '*/bin/java' -print 2>/dev/null |
  while IFS= read -r j; do readlink -f "$j"; done | sort -u > "$TMP/disk"

# 2) 실행 중인 프로세스. 호스트에서 보이지 않는 경로는 컨테이너 안의 프로세스다.
: > "$TMP/procs"
for d in /proc/[0-9]*; do
  e="$(readlink "$d/exe" 2>/dev/null)" || continue
  case "$e" in */java) echo "${d#/proc/}|$e" >> "$TMP/procs" ;; esac
done
cut -d'|' -f2 "$TMP/procs" | while IFS= read -r j; do [ -x "$j" ] && readlink -f "$j"; done | sort -u > "$TMP/procbin"
sort -u "$TMP/disk" "$TMP/procbin" > "$TMP/all"

echo "host,os,where,java_path,vendor,version,runtime_build,arch,running_pids" > "$OUT"
row() { # row <위치> <probe 결과 한 줄> <pid 목록>
  echo "$2" | awk -F'|' -v h="$HOST" -v os="$OSNAME" -v w="$1" -v pids="$3" \
    '{printf "\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\"\n", h, os, w, $1, $2, $3, $4, $5, pids}' >> "$OUT"
}
sh -c "$PROBE" < "$TMP/all" > "$TMP/probed"
while IFS= read -r line; do
  j="${line%%|*}"
  pids="$(awk -F'|' -v j="$j" '$2 == j {printf "%s ", $1}' "$TMP/procs")"
  row "host" "$line" "${pids% }"
done < "$TMP/probed"

# 3) 실행 중인 컨테이너
if [ "$NOCT" -eq 0 ] && command -v docker >/dev/null 2>&1 && docker ps >/dev/null 2>&1; then
  docker ps --format '{{.Names}}|{{.Image}}' ${CTF:+--filter "name=$CTF"} > "$TMP/cts"
  while IFS='|' read -r name image; do
    docker exec "$name" sh -c "find / -xdev \( -path /proc -o -path /sys \) -prune -o \( -type f -o -type l \) -name java -path '*/bin/java' -print 2>/dev/null | while IFS= read -r j; do readlink -f \"\$j\"; done | sort -u | { $PROBE; }" < /dev/null > "$TMP/ct" 2>/dev/null
    while IFS= read -r line; do
      [ -n "$line" ] && row "container:$name ($image)" "$line" ""
    done < "$TMP/ct"
  done < "$TMP/cts"
fi

N=$(($(wc -l < "$OUT") - 1))
echo "Java 런타임 ${N}개를 찾았습니다. 결과 파일: $OUT"
awk -F'","' 'NR > 1 {gsub(/"/, "", $9); printf "  %-44s %-22s %-18s %s%s\n", substr($3, 1, 44), substr($5, 1, 22), $7, $4, ($9 == "" ? "" : "  [실행 중 PID " $9 "]")}' "$OUT"
