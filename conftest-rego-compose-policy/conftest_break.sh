#!/usr/bin/env bash
# 정책을 일부러 깨 보고, 단위 시험이 잡아내는지 확인한다. 원본 정책은 건드리지 않고 사본으로만 시험한다.
# 준비: Docker, 같은 폴더에 compose.rego, compose_test.rego.
# 실행(Git Bash): bash conftest_break.sh   (약 10초)
export MSYS_NO_PATHCONV=1
HERE="$(pwd)"
OUT=../osk-fc-ct-out
rm -rf "$OUT"; mkdir -p "$OUT"; ABS="$(cd "$OUT" && pwd)"
cp compose.rego compose_test.rego "$OUT/"
echo "## 정책 사본에서 docker.sock 규칙의 글자를 일부러 틀리게 고침"
sed -i 's/contains(vol, "docker.sock")/contains(vol, "docker.sockX")/' "$OUT/compose.rego"
diff <(grep -n 'docker.sock' compose.rego | head -1) <(grep -n 'docker.sock' "$OUT/compose.rego" | head -1) | sed 's/^/  /'
echo "## 사본으로 단위 시험"
docker run --rm -v "$ABS:/p:ro" -w /p openpolicyagent/conftest verify -p . --no-color 2>&1 | grep -E 'FAIL|tests,' | sed 's/^/  /'
echo "  종료 코드 ${PIPESTATUS[0]}"
