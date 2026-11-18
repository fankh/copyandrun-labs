#!/bin/sh
# 사용: sh java-inventory.sh [-o 결과.csv] [-n] [-f 컨테이너이름] [-x] [찾을 폴더 ...]
#   찾을 폴더를 생략하면 / 전체를 찾는다.
#   -o  결과 CSV 파일 (기본: java-inventory-<호스트>.csv)
#   -n  컨테이너 안은 보지 않는다
#   -f  이름에 이 글자가 든 컨테이너만 본다
#   -x  인터넷에서 최신 빌드를 조회하지 않는다 (status 열이 비어 있음)
# 서버에 있는 Java 런타임을 모두 찾아 공급업체, 전체 빌드 버전, 아키텍처, 실행 중인 프로세스를 CSV 로 남기고,
# 런타임마다 지금 알려진 보안 문제를 확인한다.
#   1) 디스크의 bin/java 파일 (제품에 함께 설치된 런타임 포함)
#   2) 실행 중인 java 프로세스가 쓰는 런타임
#   3) 실행 중인 도커 컨테이너 안의 bin/java
# 런타임마다 확인하는 것:
#   latest_build, status  같은 Java 버전의 공급업체 최신 빌드(https://endoflife.date)와 비교
#                         (feature.interim.update 를 비교하고, 같으면 그 뒤 패치 번호까지 비교한다.
#                          괄호 안 날짜는 그 자료가 마지막으로 본 배포일이라, 그 뒤 공급업체 공지가 더 있을 수 있다)
#   emudhra_roots         cacerts 에 남은 eMudhra 루트 인증서 (CVE-2026-91403, CVE-2026-114820)
# 찾은 java 를 -version 으로, keytool 을 -list 로 한 번씩 실행한다. 그 밖에는 읽기만 한다.
# 모든 프로세스와 폴더를 보려면 root 로 실행한다.
OUT=""; NOCT=0; CTF=""; OFFLINE=0
while getopts "o:nf:x" o; do
  case "$o" in
    o) OUT="$OPTARG" ;;
    n) NOCT=1 ;;
    f) CTF="$OPTARG" ;;
    x) OFFLINE=1 ;;
    *) echo "사용: sh java-inventory.sh [-o 결과.csv] [-n] [-f 컨테이너이름] [-x] [찾을 폴더 ...]"; exit 2 ;;
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
TODAY="$(date +%Y-%m-%d)"
STALE="$(date -d "@$(( $(date +%s) - 120 * 86400 ))" +%Y-%m-%d 2>/dev/null)"

# probe: 표준 입력으로 받은 java 경로마다 "경로|공급업체|버전|런타임 빌드|아키텍처|eMudhra" 한 줄을 낸다.
# 컨테이너 안에서도 같은 코드를 쓰기 위해 문자열로 두고, 컨테이너 쪽 글자 깨짐을 피하려고 영문만 낸다.
PROBE='while IFS= read -r j; do
  p="$("$j" -XshowSettings:properties -version 2>&1)"
  g() { echo "$p" | sed -n "s/^ *$1 = //p" | head -1; }
  v="$(g java.version)"
  [ -n "$v" ] || v="$(echo "$p" | head -1)"
  h="${j%/bin/java}"; k="$h/lib/security/cacerts"; [ -f "$k" ] || k="$h/jre/lib/security/cacerts"
  e="unknown"
  if [ -x "$h/bin/keytool" ] && [ -f "$k" ]; then
    ow="$("$h/bin/keytool" -J-Duser.language=en -J-Duser.country=US -list -v -keystore "$k" -storepass changeit 2>/dev/null | grep "^Owner: ")"
    if [ -n "$ow" ]; then
      e=""
      for cn in "emSign Root CA - G1" "emSign Root CA - G2" "emSign ECC Root CA - G3" "AAA Certificate Services"; do
        echo "$ow" | grep -qF "CN=$cn," && e="$e${e:+; }$cn"
      done
      e="${e:-none}"
    fi
  fi
  echo "$j|$(g java.vendor)|$v|$(g java.runtime.version)|$(g os.arch)|$e"
done'

# 공급업체 이름(java.vendor) -> endoflife.date 제품 이름
product_of() {
  case "$1" in
    "Eclipse Adoptium") echo eclipse-temurin ;;
    "Oracle Corporation") echo oracle-jdk ;;
    "Amazon.com Inc.") echo amazon-corretto ;;
    "Red Hat, Inc.") echo redhat-build-of-openjdk ;;
    "Microsoft") echo microsoft-build-of-openjdk ;;
    "BellSoft") echo bellsoft-liberica ;;
    "SAP SE") echo sapmachine ;;
    "IBM Corporation") echo ibm-semeru-runtime ;;
  esac
}

# 버전 키: Java 8 은 "8 업데이트", 9 이상은 "+" 나 "-" 앞의 숫자 전부(feature interim update 패치...).
# 런타임 빌드와 공급업체 표기 모두에 쓴다.
vkey() {
  echo "$1" | awk '{
    s = $0; is8 = (s ~ /^(1\.8|8u|8\.|8$)/)
    if (!is8) sub(/[+-].*/, "", s)
    n = 0; t = s
    while (match(t, /[0-9]+/)) { a[++n] = substr(t, RSTART, RLENGTH) + 0; t = substr(t, RSTART + RLENGTH) }
    if (n == 0) exit
    if (is8) { u = 0; for (i = 1; i <= n; i++) if (a[i] >= 100) { u = a[i]; break }; print 8, u; exit }
    out = a[1] " " (n >= 2 ? a[2] : 0) " " (n >= 3 ? a[3] : 0)
    for (i = 4; i <= n; i++) out = out " " a[i]
    print out
  }'
}

# cmpbuild <런타임 키> <최신 키> -> older | newer | equal | patch(같은 업데이트에 공급업체의 뒤 패치 빌드가 있음)
cmpbuild() {
  echo "$1|$2" | awk -F'|' '{
    nk = split($1, k, " "); nl = split($2, l, " ")
    m = (k[1] == 8 && nk == 2) ? 2 : 3
    for (i = 1; i <= m; i++) { if (k[i] + 0 < l[i] + 0) { print "older"; exit } if (k[i] + 0 > l[i] + 0) { print "newer"; exit } }
    if (m == 2) { print "equal"; exit }
    if (nk > 3) {
      n = (nk > nl) ? nk : nl
      for (i = 4; i <= n; i++) { if (k[i] + 0 < l[i] + 0) { print "older"; exit } if (k[i] + 0 > l[i] + 0) { print "newer"; exit } }
      print "equal"; exit
    }
    for (i = 4; i <= nl; i++) if (l[i] + 0 > 0) { print "patch"; exit }
    print "equal"
  }'
}

# latest_status <공급업체> <런타임 빌드> -> "최신 빌드|상태"
latest_status() {
  [ "$OFFLINE" -eq 1 ] && { echo "|"; return; }
  prod="$(product_of "$1")"
  [ -n "$prod" ] || { echo "|확인 필요 (공급업체 '$1' 자료 없음. OS 패키지라면 배포판 보안 공지로 확인)"; return; }
  f="$TMP/eol-$prod"
  if [ ! -f "$f" ]; then
    { curl -fsS -m 15 "https://endoflife.date/api/$prod.json" 2>/dev/null || wget -qO- -T 15 "https://endoflife.date/api/$prod.json" 2>/dev/null; } |
      tr -d '\n' | sed 's/},[[:space:]]*{/}\n{/g' > "$f"
  fi
  [ -s "$f" ] || { echo "|확인 못 함 (최신 빌드 정보를 받지 못함)"; return; }
  key="$(vkey "$2")"
  [ -n "$key" ] || { echo "|확인 필요 (버전을 읽지 못함)"; return; }
  cyc="${key%% *}"
  line="$(grep "\"cycle\": *\"$cyc\"" "$f" | head -1)"
  [ -n "$line" ] || { echo "|확인 필요 (Java $cyc 자료 없음)"; return; }
  fld() { echo "$line" | sed -n "s/.*\"$1\": *\"\{0,1\}\([^\",}]*\)\"\{0,1\}.*/\1/p"; }
  latest="$(fld latest)"; eol="$(fld eol)"; ext="$(fld extendedSupport)"; rel="$(fld latestReleaseDate)"
  past() { case "$1" in true) return 0 ;; [0-9][0-9][0-9][0-9]-*) [ "$1" \< "$TODAY" ] ;; *) return 1 ;; esac; }
  note=""
  if past "$eol"; then
    case "$ext" in
      [0-9][0-9][0-9][0-9]-*) if past "$ext"; then echo "$latest|지원 종료 ($eol)"; return; fi
         note=" (무료 지원은 $eol 종료, 유료 연장 지원만)" ;;
      *) echo "$latest|지원 종료 ($eol)"; return ;;
    esac
  fi
  if [ -n "$STALE" ] && [ -n "$rel" ] && [ "$rel" \< "$STALE" ]; then
    echo "$latest|확인 필요 (공급업체 자료가 $rel 기준)"; return
  fi
  show="$latest ($rel)"
  case "$(cmpbuild "$key" "$(vkey "$latest")")" in
    older) echo "$show|업데이트 필요$note" ;;
    patch) echo "$show|확인 필요 (같은 업데이트에 공급업체의 뒤 패치 빌드가 있음)$note" ;;
    *) echo "$show|최신 ($rel 자료 기준)$note" ;;
  esac
}

emudhra_ko() {
  case "$1" in
    none) echo "없음" ;;
    unknown|"") echo "확인 못 함 (keytool 또는 cacerts 없음)" ;;
    *) echo "남아 있음: $1" ;;
  esac
}

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

echo "host,os,where,java_path,vendor,version,runtime_build,arch,running_pids,latest_build,status,emudhra_roots" > "$OUT"
csvq() { printf '"%s"' "$(echo "$1" | sed 's/"/""/g')"; }
row() { # row <위치> <probe 결과 한 줄> <pid 목록>
  IFS='|' read -r jp ven ver bld arc emu <<EOF_ROW
$2
EOF_ROW
  ls="$(latest_status "$ven" "$bld")"
  for v in "$HOST" "$OSNAME" "$1" "$jp" "$ven" "$ver" "$bld" "$arc" "$3" "${ls%%|*}" "${ls#*|}"; do csvq "$v"; printf ','; done >> "$OUT"
  csvq "$(emudhra_ko "$emu")" >> "$OUT"; echo >> "$OUT"
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
awk -F'","' 'NR > 1 {gsub(/"/, "", $9); gsub(/"$/, "", $12); printf "  %-36s %-18s %-16s %-14s %s | eMudhra: %s%s\n", substr($3, 1, 36), substr($5, 1, 18), $7, $10, $11, $12, ($9 == "" ? "" : "  [실행 중 PID " $9 "]")}' "$OUT"
