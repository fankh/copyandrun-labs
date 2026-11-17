#!/usr/bin/env bash
# llama-bench 심화: 입력 길이(pp)별 속도, 출력 길이(tg)별 속도, 플래시 어텐션(-fa) 켜기/끄기 비교. 모두 3회 평균.
# 준비: llama.cpp Vulkan 빌드(llama-bench.exe), GGUF 모델(Qwen2.5-7B)
# 실행(Git Bash): bash bench_more.sh   (약 2분)
LLAMA=/c/llama.cpp
M7=/c/models/Qwen2.5-7B-Instruct-Q4_K_M.gguf
cd "$LLAMA" || exit 1

show() {   # llama-bench 표에서 시험 이름과 속도 열만 보여 준다
  tr -d '\r' | awk -F'|' '$2 ~ /qwen|llama/ {gsub(/^ +| +$/, "", $7); gsub(/^ +/, "", $8); gsub(/^ +| +$/, "", $6); printf "  %-14s %s\n", $7 (NF>9 ? " fa=" $8 : ""), (NF>9 ? $9 : $8)}'
}

echo "## 1. 입력 길이(pp)에 따른 입력 읽기 속도(7B, 출력 없음 -n 0)"
./llama-bench.exe -m "$M7" -p 128,512,2048,4096 -n 0 -r 3 2>/dev/null | show

echo "## 2. 출력 길이(tg)에 따른 생성 속도(7B, 입력 없음 -p 0)"
./llama-bench.exe -m "$M7" -p 0 -n 16,64,256 -r 3 2>/dev/null | show

echo "## 3. 플래시 어텐션(-fa 0/1): 긴 입력 2048과 4096 에서"
./llama-bench.exe -m "$M7" -p 2048,4096 -n 32 -fa 0,1 -r 3 2>/dev/null | show
