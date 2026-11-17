# llama-server로 내 PC에 OpenAI 호환 API 열기

llama.cpp의 llama-server에 GGUF 모델을 올려 OpenAI와 같은 형식의 /v1/chat/completions 주소를 만듭니다. 127.0.0.1에만 열고, requests와 openai 파이썬 라이브러리로 호출해 한 번에 받기와 스트리밍을 확인합니다.

글: https://copyandrun.com/blog/llama-server-openai-compatible-api/

## 파일

- `server_demo.py`

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
