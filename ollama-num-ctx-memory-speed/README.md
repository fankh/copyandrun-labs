# Ollama num_ctx를 키우면 메모리는 얼마나 늘까: 2K, 8K, 32K 측정

같은 2.4B 모델을 컨텍스트 길이 2048, 8192, 32768로 올려 보고 ollama ps의 메모리 사용량, 불러오는 시간, 생성 속도를 비교합니다. 긴 문서를 다루려고 num_ctx를 키울 때 치르는 비용을 숫자로 봅니다.

## 링크

- 글: [https://copyandrun.com/blog/ollama-num-ctx-memory-speed/](https://copyandrun.com/blog/ollama-num-ctx-memory-speed/)
- 한 번에 받기: [ollama-num-ctx-memory-speed.zip](https://copyandrun.com/code-zip/ollama-num-ctx-memory-speed.zip)
- GitHub 폴더: [copyandrun-labs/ollama-num-ctx-memory-speed](https://github.com/fankh/copyandrun-labs/tree/main/ollama-num-ctx-memory-speed)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `ctx_more.py` | <a href="https://fankh.github.io/copyandrun-labs/ollama-num-ctx-memory-speed/ctx_more.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/ollama-num-ctx-memory-speed/ctx_more.py) |
| `ctx_test.py` | <a href="https://fankh.github.io/copyandrun-labs/ollama-num-ctx-memory-speed/ctx_test.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/ollama-num-ctx-memory-speed/ctx_test.py) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
