# Hermes Agent의 명령 승인 절차 확인하기

연습용 폴더에서 재귀 삭제를 시켜 보며 Hermes Agent의 smart와 manual 승인 방식, 거부 후 에이전트의 반응, 영구 허용 목록의 범위, deny 규칙, 일회성 실행의 승인 우회를 직접 확인하고, 컨테이너 격리와 터미널 백엔드의 관계를 정리합니다.

## 링크

- 글: [https://copyandrun.com/blog/hermes-agent-command-approval/](https://copyandrun.com/blog/hermes-agent-command-approval/)
- 한 번에 받기: [hermes-agent-command-approval.zip](https://copyandrun.com/code-zip/hermes-agent-command-approval.zip)
- GitHub 폴더: [copyandrun-labs/hermes-agent-command-approval](https://github.com/fankh/copyandrun-labs/tree/main/hermes-agent-command-approval)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `docker-compose.yml` | <a href="https://fankh.github.io/copyandrun-labs/hermes-agent-command-approval/docker-compose.yml" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/hermes-agent-command-approval/docker-compose.yml) |
| `Dockerfile` | <a href="https://fankh.github.io/copyandrun-labs/hermes-agent-command-approval/Dockerfile" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/hermes-agent-command-approval/Dockerfile) |
| `reset-practice.sh` | <a href="https://fankh.github.io/copyandrun-labs/hermes-agent-command-approval/reset-practice.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/hermes-agent-command-approval/reset-practice.sh) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
