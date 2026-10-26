# MCP 도구 설명이 승인 뒤에 바뀌는 rug pull 탐지하기

처음 승인할 때는 멀쩡하던 MCP 서버가 도구 설명만 바꿔 숨은 지시문을 심는 경우를 직접 재현합니다. tools/list 결과를 SHA-256 으로 고정해 어느 도구의 어느 필드가 바뀌었는지 diff 로 알려 주는 점검 스크립트를 만들고, 이 방법이 막지 못하는 경우도 정직하게 확인합니다.

글: https://copyandrun.com/blog/mcp-rug-pull-tool-description-pinning/

## 파일

- `compose.yaml`
- `Dockerfile`
- `pin_check.py`
- `report_app.py`
- `server_v1.py`
- `server_v2.py`

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
