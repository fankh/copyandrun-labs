#!/usr/bin/env bash
# Hadolint 로 Dockerfile 을 점검한다: 나쁜 파일의 지적, 고친 파일, 실패 기준, 예외 설정, 고친 파일 빌드.
# 준비: Docker, 파이썬(집계용). Hadolint 는 컨테이너로 실행한다.
# 실행(Git Bash): bash lint_demo.sh   (약 1분)
set -u
export MSYS_NO_PATHCONV=1
H="docker run --rm -i hadolint/hadolint hadolint"

count() { python -X utf8 -c "
import json, sys
from collections import Counter
d = json.load(sys.stdin)
c = Counter(x['level'] for x in d)
print('지적', len(d), '건', dict(c))
"; }

echo "## 1. 나쁜 Dockerfile 점검(Dockerfile.bad, 아홉 줄)"
cat Dockerfile.bad
echo "---"
$H --no-color - < Dockerfile.bad | sed 's/^-:/줄 /'
echo "## 2. 수준별 집계(JSON 출력)"
$H -f json - < Dockerfile.bad 2>/dev/null | count

echo "## 3. 고친 Dockerfile 점검(Dockerfile.good)"
$H --no-color - < Dockerfile.good; echo "종료 코드: $?"

echo "## 4. 종료 코드: 어느 수준부터 실패로 볼까(--failure-threshold)"
echo "(Dockerfile.warnonly 는 warning 한 건과 info 한 건만 있는 파일, Dockerfile.bad 는 error 가 있는 파일)"
$H --no-color - < Dockerfile.warnonly | sed 's/^-:/줄 /'
for f in Dockerfile.warnonly Dockerfile.bad; do
  for t in error warning info; do
    $H --failure-threshold $t - < $f >/dev/null 2>&1; echo "$f threshold=$t 종료 코드: $?"
  done
done

echo "## 5. 예외 설정(.hadolint.yaml): DL3059(RUN 합치기), DL3009(apt 목록 삭제) 제외"
printf 'ignored:\n  - DL3059\n  - DL3009\n' > .hadolint.yaml
docker run --rm -i -v "$(pwd -W 2>/dev/null || pwd)/.hadolint.yaml:/.config/hadolint.yaml:ro" hadolint/hadolint hadolint -f json - < Dockerfile.bad 2>/dev/null | count
rm -f .hadolint.yaml

echo "## 6. 고친 Dockerfile 을 실제로 빌드하고 실행"
docker build -q -f Dockerfile.good -t osk-hadolint-good . >/dev/null && echo "빌드 성공"
echo "실행 사용자: $(docker run --rm osk-hadolint-good id -u)"
echo "앱 출력: $(docker run --rm osk-hadolint-good)"
docker image inspect osk-hadolint-good --format '크기 {{.Size}} 바이트, 사용자 {{.Config.User}}, 헬스체크 {{if .Config.Healthcheck}}있음{{else}}없음{{end}}'
docker rmi -f osk-hadolint-good >/dev/null && echo "시험 이미지 삭제"
