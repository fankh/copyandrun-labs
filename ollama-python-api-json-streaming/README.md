# 파이썬에서 로컬 Ollama API 호출하기: 응답 받기, JSON 형식 고정, 스트리밍

requests만으로 내 PC의 Ollama를 호출합니다. 한 번에 받기, 옵션 넘기기, JSON 스키마로 출력 형식 고정하기, 글자가 나오는 대로 받는 스트리밍을 실행해 결과를 확인합니다. 한글이 깨지는 Windows 함정도 함께 정리합니다.

## 링크

- 글: [https://copyandrun.com/blog/ollama-python-api-json-streaming/](https://copyandrun.com/blog/ollama-python-api-json-streaming/)
- 한 번에 받기: [ollama-python-api-json-streaming.zip](https://copyandrun.com/code-zip/ollama-python-api-json-streaming.zip)
- GitHub 폴더: [copyandrun-labs/ollama-python-api-json-streaming](https://github.com/fankh/copyandrun-labs/tree/main/ollama-python-api-json-streaming)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `api_demo.py` | <a href="https://fankh.github.io/copyandrun-labs/ollama-python-api-json-streaming/api_demo.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/ollama-python-api-json-streaming/api_demo.py) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
