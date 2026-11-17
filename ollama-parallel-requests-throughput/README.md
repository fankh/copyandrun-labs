# Ollama에 동시에 질문 여러 개 보내면: 1, 2, 4, 8개 요청 처리량 재기

같은 모델에 요청을 1개, 2개, 4개, 8개 동시에 보내 전체 처리 시간과 요청당 속도를 잽니다. 이 PC에서는 요청당 생성 속도가 거의 그대로이고 대기 시간만 늘어, 요청이 줄을 서서 처리되는 것으로 추정합니다.

## 링크

- 글: [https://copyandrun.com/blog/ollama-parallel-requests-throughput/](https://copyandrun.com/blog/ollama-parallel-requests-throughput/)
- 한 번에 받기: [ollama-parallel-requests-throughput.zip](https://copyandrun.com/code-zip/ollama-parallel-requests-throughput.zip)
- GitHub 폴더: [copyandrun-labs/ollama-parallel-requests-throughput](https://github.com/fankh/copyandrun-labs/tree/main/ollama-parallel-requests-throughput)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `parallel_more.py` | <a href="https://fankh.github.io/copyandrun-labs/ollama-parallel-requests-throughput/parallel_more.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/ollama-parallel-requests-throughput/parallel_more.py) |
| `parallel_test.py` | <a href="https://fankh.github.io/copyandrun-labs/ollama-parallel-requests-throughput/parallel_test.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/ollama-parallel-requests-throughput/parallel_test.py) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
