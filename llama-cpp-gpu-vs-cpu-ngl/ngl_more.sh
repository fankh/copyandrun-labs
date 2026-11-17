#!/usr/bin/env bash
# llama-bench 로 CPU 로만 돌릴 때(-ngl 0) 스레드 수(-t)에 따라 속도가 어떻게 달라지는지, 1B 모델로 잰다. 모두 3회 평균.
# 준비: llama.cpp Vulkan 빌드(llama-bench.exe), Llama-3.2-1B GGUF. 이 PC 는 논리 코어 32개.
# -nopo(--no-op-offload)는 -ngl 0 이어도 입력을 읽을 때 그래픽을 쓰는 동작을 끈다.
# 실행(Git Bash): bash ngl_more.sh   (약 2분)
LLAMA=/c/llama.cpp
M1=/c/models/Llama-3.2-1B-Instruct-Q4_K_M.gguf
cd "$LLAMA" || exit 1

# 표의 뒤쪽 두 열(시험 이름, 속도)과 7번째 열(스레드 수)만 한 줄로 보여 준다
show() {
  tr -d '\r' | awk -F'|' '$2 ~ /llama|qwen/ {t=$(NF-2); v=$(NF-1); gsub(/^ +| +$/, "", $7); gsub(/^ +| +$/, "", t); gsub(/^ +| +$/, "", v); printf "  threads=%-3s %-6s %s\n", $7, t, v}'
}

echo "## 1. CPU 만(-ngl 0): 스레드 수별 속도(pp256 읽기, tg32 생성)"
./llama-bench.exe -m "$M1" -ngl 0 -t 1,2,4,8,16,32 -p 256 -n 32 -r 3 2>/dev/null | show

echo "## 2. 같은 CPU 시험에서 입력 읽기의 그래픽 도움을 끄기(-nopo 1)"
./llama-bench.exe -m "$M1" -ngl 0 -nopo 1 -t 4,16,32 -p 256 -n 0 -r 3 2>/dev/null | show

echo "## 3. 같은 모델을 그래픽으로(-ngl 99) 한 번 재서 비교"
./llama-bench.exe -m "$M1" -ngl 99 -p 256 -n 32 -r 3 2>/dev/null | tr -d '\r' | awk -F'|' '$2 ~ /llama/ {t=$(NF-2); v=$(NF-1); gsub(/^ +| +$/, "", t); gsub(/^ +| +$/, "", v); printf "  GPU(ngl 99)   %-6s %s\n", t, v}'
