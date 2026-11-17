# llama.cpp와 GGUF 파일로 내 PC 속도 재기: llama-bench로 1B와 7B 비교

Ollama 없이 llama.cpp의 llama-bench로 GGUF 모델을 직접 재 봅니다. 내장 그래픽의 Vulkan으로 1B와 7B 모델의 입력 읽기 속도와 생성 속도를 3회 평균으로 비교하고, 파일 크기에서 양자화 비트 수를 계산하는 전체 스크립트를 실행합니다.

## 링크

- 글: [https://copyandrun.com/blog/llama-cpp-vulkan-bench-gguf/](https://copyandrun.com/blog/llama-cpp-vulkan-bench-gguf/)
- 한 번에 받기: [llama-cpp-vulkan-bench-gguf.zip](https://copyandrun.com/code-zip/llama-cpp-vulkan-bench-gguf.zip)
- GitHub 폴더: [copyandrun-labs/llama-cpp-vulkan-bench-gguf](https://github.com/fankh/copyandrun-labs/tree/main/llama-cpp-vulkan-bench-gguf)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `bench_gguf.sh` | <a href="https://fankh.github.io/copyandrun-labs/llama-cpp-vulkan-bench-gguf/bench_gguf.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/llama-cpp-vulkan-bench-gguf/bench_gguf.sh) |
| `bench_more.sh` | <a href="https://fankh.github.io/copyandrun-labs/llama-cpp-vulkan-bench-gguf/bench_more.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/llama-cpp-vulkan-bench-gguf/bench_more.sh) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
