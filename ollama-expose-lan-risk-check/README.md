# Ollama를 0.0.0.0으로 열면 생기는 일: 인증 없는 로컬 AI 서버 점검

기본 설치의 Ollama는 127.0.0.1에만 열립니다. 별도 임시 인스턴스를 OLLAMA_HOST=0.0.0.0으로 띄워 같은 PC의 네트워크 주소로 접속해 보고, 로그인 없이 모델 목록이 보이는 것을 확인한 뒤 되돌립니다.

## 링크

- 글: [https://copyandrun.com/blog/ollama-expose-lan-risk-check/](https://copyandrun.com/blog/ollama-expose-lan-risk-check/)
- 한 번에 받기: [ollama-expose-lan-risk-check.zip](https://copyandrun.com/code-zip/ollama-expose-lan-risk-check.zip)
- GitHub 폴더: [copyandrun-labs/ollama-expose-lan-risk-check](https://github.com/fankh/copyandrun-labs/tree/main/ollama-expose-lan-risk-check)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `cors_more.py` | <a href="https://fankh.github.io/copyandrun-labs/ollama-expose-lan-risk-check/cors_more.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/ollama-expose-lan-risk-check/cors_more.py) |
| `expose_check.py` | <a href="https://fankh.github.io/copyandrun-labs/ollama-expose-lan-risk-check/expose_check.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/ollama-expose-lan-risk-check/expose_check.py) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
