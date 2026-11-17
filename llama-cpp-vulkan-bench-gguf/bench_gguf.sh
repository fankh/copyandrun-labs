#!/usr/bin/env bash
# llama-bench 로 GGUF 모델 두 개의 입력 읽기(pp)와 생성(tg) 속도를 3회 평균으로 재고, 파일 크기에서 비트 수를 계산한다.
# 준비: llama.cpp Vulkan 빌드(llama-bench.exe), GGUF 모델 두 개, 파이썬(비트 수 계산용)
# 실행(Git Bash): bash bench_gguf.sh   (약 1분)
LLAMA=/c/llama.cpp
M1=/c/models/Llama-3.2-1B-Instruct-Q4_K_M.gguf
M7=/c/models/Qwen2.5-7B-Instruct-Q4_K_M.gguf

cd "$LLAMA" || exit 1

echo "## 1. 그래픽 장치"
./llama-bench.exe -m "$M1" -p 16 -n 1 -r 1 2>&1 | tr -d '\r' | grep -E 'Found|uma' | cut -c1-110

echo "## 2. 속도(3회 평균, 표준편차 포함)"
./llama-bench.exe -m "$M1" -m "$M7" -p 512 -n 64 -r 3 2>/dev/null | tr -d '\r' |
  awk -F'|' '$2 ~ /llama|qwen/ {gsub(/^ +| +$/, "", $2); gsub(/^ +| +$/, "", $3); gsub(/ +/, "", $7); gsub(/^ +/, "", $8); printf "%-24s %-10s %-6s %s\n", $2, $3, $7, $8}'

echo "## 3. 파일 크기에서 계산한 값 하나당 비트 수"
python -X utf8 - <<'PY'
# (이름, 파일 크기 GiB, 매개변수 B) -- 2번 표의 size, params 열 값
for name, gib, b in (("1B", 762.81 / 1024, 1.24), ("7B", 4.36, 7.62)):
    print(f"{name}: {gib * 2**30 * 8 / (b * 1e9):.2f} 비트")
PY
