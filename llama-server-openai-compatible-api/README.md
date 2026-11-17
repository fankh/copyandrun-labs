# llama-server로 내 PC에 OpenAI 호환 API 열기

llama.cpp의 llama-server에 GGUF 모델을 올려 OpenAI와 같은 형식의 /v1/chat/completions 주소를 만듭니다. 127.0.0.1에만 열고, requests와 openai 파이썬 라이브러리로 호출해 한 번에 받기와 스트리밍을 확인합니다.

## 링크

- 글: [https://copyandrun.com/blog/llama-server-openai-compatible-api/](https://copyandrun.com/blog/llama-server-openai-compatible-api/)
- 한 번에 받기: [llama-server-openai-compatible-api.zip](https://copyandrun.com/code-zip/llama-server-openai-compatible-api.zip)
- GitHub 폴더: [copyandrun-labs/llama-server-openai-compatible-api](https://github.com/fankh/copyandrun-labs/tree/main/llama-server-openai-compatible-api)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `server_demo.py` | <a href="https://fankh.github.io/copyandrun-labs/llama-server-openai-compatible-api/server_demo.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/llama-server-openai-compatible-api/server_demo.py) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
