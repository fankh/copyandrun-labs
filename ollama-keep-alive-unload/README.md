# Ollama keep_alive: 모델을 메모리에 얼마나 올려 둘지 정하기

Ollama는 모델을 한 번 쓰면 일정 시간 메모리에 남겨 둡니다. keep_alive를 0, 20초, 무기한으로 바꿔 가며 ollama ps의 UNTIL 열과 다음 호출의 불러오는 시간이 어떻게 달라지는지 직접 확인합니다.

## 링크

- 글: [https://copyandrun.com/blog/ollama-keep-alive-unload/](https://copyandrun.com/blog/ollama-keep-alive-unload/)
- 한 번에 받기: [ollama-keep-alive-unload.zip](https://copyandrun.com/code-zip/ollama-keep-alive-unload.zip)
- GitHub 폴더: [copyandrun-labs/ollama-keep-alive-unload](https://github.com/fankh/copyandrun-labs/tree/main/ollama-keep-alive-unload)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `keep_alive_more.py` | <a href="https://fankh.github.io/copyandrun-labs/ollama-keep-alive-unload/keep_alive_more.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/ollama-keep-alive-unload/keep_alive_more.py) |
| `keep_alive_test.py` | <a href="https://fankh.github.io/copyandrun-labs/ollama-keep-alive-unload/keep_alive_test.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/ollama-keep-alive-unload/keep_alive_test.py) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
