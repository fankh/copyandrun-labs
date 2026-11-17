# llama.cpp -ngl로 그래픽 가속 켜고 끄기: 1B와 7B 속도 차이와 중간 값 측정

llama-bench의 -ngl 값을 99와 0으로 바꿔 1B와 7B 모델을 재고, 7B는 28층 중 0, 7, 14, 21, 28층만 올린 중간 값도 잽니다. 생성 속도는 2.6배에서 3.2배, 입력 읽기는 2.2배에서 3.1배 차이가 났고, 처음 측정값이 반복 측정에서 재현되지 않은 부분도 정정합니다.

## 링크

- 글: [https://copyandrun.com/blog/llama-cpp-gpu-vs-cpu-ngl/](https://copyandrun.com/blog/llama-cpp-gpu-vs-cpu-ngl/)
- 한 번에 받기: [llama-cpp-gpu-vs-cpu-ngl.zip](https://copyandrun.com/code-zip/llama-cpp-gpu-vs-cpu-ngl.zip)
- GitHub 폴더: [copyandrun-labs/llama-cpp-gpu-vs-cpu-ngl](https://github.com/fankh/copyandrun-labs/tree/main/llama-cpp-gpu-vs-cpu-ngl)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `ngl_bench.sh` | <a href="https://fankh.github.io/copyandrun-labs/llama-cpp-gpu-vs-cpu-ngl/ngl_bench.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/llama-cpp-gpu-vs-cpu-ngl/ngl_bench.sh) |
| `ngl_more.sh` | <a href="https://fankh.github.io/copyandrun-labs/llama-cpp-gpu-vs-cpu-ngl/ngl_more.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/llama-cpp-gpu-vs-cpu-ngl/ngl_more.sh) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
