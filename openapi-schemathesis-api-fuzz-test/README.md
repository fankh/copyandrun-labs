# OpenAPI 명세로 API 자동 시험: Schemathesis로 500 오류 찾기

직접 만든 작은 FastAPI 연습용 API에 입력 검증 없는 정수 파라미터와 명세와 다른 응답 형식을 일부러 넣고, Schemathesis가 어떤 입력으로 어떤 실패(500 오류, 응답 스키마 위반, 문서에 없는 상태 코드)를 찾는지 봅니다. 수정한 뒤 같은 명령이 통과하는 과정까지 로컬에서 따라 합니다.

글: https://copyandrun.com/blog/openapi-schemathesis-api-fuzz-test/

## 파일

- `app_v1.py`
- `app_v2.py`
- `run_server.sh`

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
