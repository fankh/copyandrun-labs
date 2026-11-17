# API 과다 응답 걸러 내기: FastAPI response_model과 응답 필드 점검 게이트

저장된 사용자 기록을 그대로 반환하는 연습용 FastAPI 앱에서 해시된 비밀번호, 내부 메모, 다른 사용자의 이메일과 전화번호까지 응답에 나가는 것을 curl로 확인합니다. 응답 모델로 고친 수정판과 비교하고, 허용 필드 목록 대조와 민감 키 이름 탐지를 하는 점검 스크립트를 CI 게이트로 붙입니다.

글: https://copyandrun.com/blog/api-excessive-data-exposure-response-filter/

## 파일

- `check_fields.py`
- `Dockerfile`
- `fixed_app.py`
- `requirements.txt`
- `vulnerable_app.py`

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
