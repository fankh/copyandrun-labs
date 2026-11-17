#!/usr/bin/env bash
# Syft 심화: 폴더 스캔, 출력 형식 비교, 이미지 두 개의 차이, 레이어 범위(scope) 비교.
# 준비: Docker, 파이썬(결과 집계용). Syft 는 컨테이너로 실행한다.
# 실행(Git Bash): bash syft_more.sh   (약 2분)
set -u
export MSYS_NO_PATHCONV=1
HERE="$(pwd -W 2>/dev/null || pwd)"
SYFT="docker run --rm anchore/syft:latest"

echo "## 1. 폴더 스캔: 작은 예제 프로젝트(requirements.txt 와 package-lock.json)"
rm -rf sample && mkdir sample
printf 'requests==2.19.1\nflask==1.0\n' > sample/requirements.txt
cat > sample/package-lock.json <<'JSON'
{"name":"demo","version":"1.0.0","lockfileVersion":3,"requires":true,
 "packages":{"":{"name":"demo","version":"1.0.0","dependencies":{"left-pad":"1.3.0"}},
             "node_modules/left-pad":{"version":"1.3.0","resolved":"https://registry.npmjs.org/left-pad/-/left-pad-1.3.0.tgz"}}}
JSON
docker run --rm -v "$HERE/sample:/src:ro" anchore/syft:latest dir:/src -o table 2>/dev/null

echo "## 2. 출력 형식별 크기(python:3.12-alpine)"
for f in syft-json cyclonedx-json spdx-json; do
  $SYFT python:3.12-alpine -o $f 2>/dev/null > "out-$f.json"
  printf '%-16s %8s bytes\n' $f "$(wc -c < out-$f.json | tr -d ' ')"
done

echo "## 3. 이미지 두 개의 차이: python:3.12-alpine 과 python:3.9-alpine"
$SYFT python:3.9-alpine -o cyclonedx-json 2>/dev/null > out-39.json
python -X utf8 - <<'PY'
import json
def pk(f):
    return {(c["name"], c.get("version", "")) for c in json.load(open(f, encoding="utf-8"))["components"] if c["type"] == "library"}
a, b = pk("out-cyclonedx-json.json"), pk("out-39.json")
print("3.12 패키지", len(a), "/ 3.9 패키지", len(b))
print("양쪽에 같은 이름·버전:", len(a & b))
na, nb = {n for n, _ in a}, {n for n, _ in b}
print("이름은 같은데 버전이 다른 것:", len({n for n, _ in a - b} & {n for n, _ in b - a}))
print("3.12 에만 있는 이름:", sorted(na - nb)[:6])
print("3.9 에만 있는 이름:", sorted(nb - na)[:6])
PY

echo "## 4. 범위(scope): 최종 이미지(squashed)와 모든 레이어(all-layers)"
for s in squashed all-layers; do
  n=$($SYFT python:3.12-alpine --scope $s -o cyclonedx-json 2>/dev/null | python -X utf8 -c "import json,sys; print(len(json.load(sys.stdin)['components']))")
  echo "scope=$s 구성 요소 $n"
done
rm -rf sample out-*.json
