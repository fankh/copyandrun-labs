# Hermes Agent에 MCP filesystem 서버를 붙이고 접근 범위 제한하기

공식 filesystem MCP 서버를 Hermes Agent에 연결하고 읽기 도구 7개만 노출한 뒤, 허용 폴더 밖 접근이 서버에서 거부되는 것을 확인합니다. 내장 파일 도구와 하위 에이전트, 예약 작업이 이 제한을 우회하려는 모습을 실제로 보고 함께 끄는 방법까지 다룹니다.

글: https://copyandrun.com/blog/hermes-agent-mcp-filesystem/

## 파일

- `docker-compose.yml`
- `Dockerfile`
- `limit-tools.sh`
- `seed-files.sh`
- `setup-mcp.sh`

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
