# Hermes Agent에 MCP filesystem 서버를 붙이고 접근 범위 제한하기

공식 filesystem MCP 서버를 Hermes Agent에 연결하고 읽기 도구 7개만 노출한 뒤, 허용 폴더 밖 접근이 서버에서 거부되는 것을 확인합니다. 내장 파일 도구와 하위 에이전트, 예약 작업이 이 제한을 우회하려는 모습을 실제로 보고 함께 끄는 방법까지 다룹니다.

## 링크

- 글: [https://copyandrun.com/blog/hermes-agent-mcp-filesystem/](https://copyandrun.com/blog/hermes-agent-mcp-filesystem/)
- 한 번에 받기: [hermes-agent-mcp-filesystem.zip](https://copyandrun.com/code-zip/hermes-agent-mcp-filesystem.zip)
- GitHub 폴더: [copyandrun-labs/hermes-agent-mcp-filesystem](https://github.com/fankh/copyandrun-labs/tree/main/hermes-agent-mcp-filesystem)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `docker-compose.yml` | <a href="https://fankh.github.io/copyandrun-labs/hermes-agent-mcp-filesystem/docker-compose.yml" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/hermes-agent-mcp-filesystem/docker-compose.yml) |
| `Dockerfile` | <a href="https://fankh.github.io/copyandrun-labs/hermes-agent-mcp-filesystem/Dockerfile" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/hermes-agent-mcp-filesystem/Dockerfile) |
| `limit-tools.sh` | <a href="https://fankh.github.io/copyandrun-labs/hermes-agent-mcp-filesystem/limit-tools.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/hermes-agent-mcp-filesystem/limit-tools.sh) |
| `seed-files.sh` | <a href="https://fankh.github.io/copyandrun-labs/hermes-agent-mcp-filesystem/seed-files.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/hermes-agent-mcp-filesystem/seed-files.sh) |
| `setup-mcp.sh` | <a href="https://fankh.github.io/copyandrun-labs/hermes-agent-mcp-filesystem/setup-mcp.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/hermes-agent-mcp-filesystem/setup-mcp.sh) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
