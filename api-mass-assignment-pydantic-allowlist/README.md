# API 대량 할당 막기: FastAPI Pydantic extra=forbid

요청 JSON을 그대로 사용자 기록에 합치는 연습용 FastAPI 앱에서 일반 사용자가 role을 admin으로 올리는 과정을 curl로 확인합니다. 같은 API를 Pydantic 허용 필드 모델로 고치면 422로 거절되는 것을 비교하고, 회귀를 막는 pytest 게이트를 붙입니다.

## 링크

- 글: [https://copyandrun.com/blog/api-mass-assignment-pydantic-allowlist/](https://copyandrun.com/blog/api-mass-assignment-pydantic-allowlist/)
- 한 번에 받기: [api-mass-assignment-pydantic-allowlist.zip](https://copyandrun.com/code-zip/api-mass-assignment-pydantic-allowlist.zip)
- GitHub 폴더: [copyandrun-labs/api-mass-assignment-pydantic-allowlist](https://github.com/fankh/copyandrun-labs/tree/main/api-mass-assignment-pydantic-allowlist)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `Dockerfile` | <a href="https://fankh.github.io/copyandrun-labs/api-mass-assignment-pydantic-allowlist/Dockerfile" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/api-mass-assignment-pydantic-allowlist/Dockerfile) |
| `fixed_app.py` | <a href="https://fankh.github.io/copyandrun-labs/api-mass-assignment-pydantic-allowlist/fixed_app.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/api-mass-assignment-pydantic-allowlist/fixed_app.py) |
| `requirements.txt` | <a href="https://fankh.github.io/copyandrun-labs/api-mass-assignment-pydantic-allowlist/requirements.txt" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/api-mass-assignment-pydantic-allowlist/requirements.txt) |
| `test_gate.py` | <a href="https://fankh.github.io/copyandrun-labs/api-mass-assignment-pydantic-allowlist/test_gate.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/api-mass-assignment-pydantic-allowlist/test_gate.py) |
| `vulnerable_app.py` | <a href="https://fankh.github.io/copyandrun-labs/api-mass-assignment-pydantic-allowlist/vulnerable_app.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/api-mass-assignment-pydantic-allowlist/vulnerable_app.py) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
