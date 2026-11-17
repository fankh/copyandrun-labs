#!/usr/bin/env bash
# llama-bench 로 -ngl(그래픽에 올릴 층 수)을 바꿔 가며 입력 읽기(pp)와 생성(tg) 속도를 잰다.
# 준비: llama.cpp Vulkan 빌드(llama-bench.exe)와 GGUF 모델 두 개.
# 실행(Git Bash): bash ngl_bench.sh
LLAMA=/c/llama.cpp
M1=/c/models/Llama-3.2-1B-Instruct-Q4_K_M.gguf
M7=/c/models/Qwen2.5-7B-Instruct-Q4_K_M.gguf

cd "$LLAMA" || exit 1

# llama-bench 의 표에서 모델, ngl, 테스트, 속도 열만 한 줄로 줄여 보여 준다.
bench() {
  ./llama-bench.exe "$@" 2>/dev/null | tr -d '\r' |
    awk -F'|' '$2 ~ /llama|qwen/ {gsub(/^ +| +$/, "", $2); gsub(/ +/, "", $7); gsub(/^ +/, "", $8); printf "%-24s ngl=%-3d %-6s %s\n", $2, $6, $7, $8}'
}

echo "## 1. 두 값 비교: 99(전부 그래픽)와 0(하나도 안 올림)"
bench -m "$M1" -m "$M7" -ngl 99 -p 256 -n 32 -r 1
bench -m "$M1" -m "$M7" -ngl 0  -p 256 -n 32 -r 1

echo "## 2. 7B 중간 값: 28층 모델에서 일부만 올리기"
bench -m "$M7" -ngl 0,7,14,21,28 -p 256 -n 32 -r 1
