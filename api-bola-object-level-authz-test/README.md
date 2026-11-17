# API BOLA 점검: 로그인한 사용자가 남의 주문 번호로 조회되는지 직접 시험하기

BOLA는 로그인은 했지만 남의 객체 번호를 넣어도 조회되는 API 권한 검증 누락입니다. 127.0.0.1에 시험용 주문 API를 임시로 띄워 같은 요청이 취약한 판에서는 200, 고친 판에서는 404가 되는 것을 Python 스크립트로 확인합니다.

## 링크

- 글: [https://copyandrun.com/blog/api-bola-object-level-authz-test/](https://copyandrun.com/blog/api-bola-object-level-authz-test/)
- 한 번에 받기: [api-bola-object-level-authz-test.zip](https://copyandrun.com/code-zip/api-bola-object-level-authz-test.zip)
- GitHub 폴더: [copyandrun-labs/api-bola-object-level-authz-test](https://github.com/fankh/copyandrun-labs/tree/main/api-bola-object-level-authz-test)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `bola_lab.py` | <a href="https://fankh.github.io/copyandrun-labs/api-bola-object-level-authz-test/bola_lab.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/api-bola-object-level-authz-test/bola_lab.py) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
