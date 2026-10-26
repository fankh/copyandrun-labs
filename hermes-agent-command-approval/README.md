# Hermes Agent의 명령 승인 흐름 확인하기

연습용 폴더에서 재귀 삭제를 시켜 보며 Hermes Agent의 smart와 manual 승인 방식, 거부 후 에이전트의 반응, 영구 허용 목록의 범위, deny 규칙, 일회성 실행의 승인 우회를 직접 확인하고, 컨테이너 격리와 터미널 백엔드의 관계를 정리합니다.

글: https://copyandrun.com/blog/hermes-agent-command-approval/

## 파일

- `docker-compose.yml`
- `Dockerfile`
- `reset-practice.sh`

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
