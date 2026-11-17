# Hermes Agent의 스킬과 메모리, 저장되는 정보 확인하기

세션을 닫고 새로 열어도 메모리가 남는지, 에이전트가 만든 스킬을 슬래시 명령으로 다시 쓸 수 있는지 확인하고, ~/.hermes 안에 대화와 입력 기록이 어디에 남는지 찾아 가짜 토큰 문자열로 저장 위험과 정리 방법을 점검합니다.

## 링크

- 글: [https://copyandrun.com/blog/hermes-agent-skills-and-memory/](https://copyandrun.com/blog/hermes-agent-skills-and-memory/)
- 한 번에 받기: [hermes-agent-skills-and-memory.zip](https://copyandrun.com/code-zip/hermes-agent-skills-and-memory.zip)
- GitHub 폴더: [copyandrun-labs/hermes-agent-skills-and-memory](https://github.com/fankh/copyandrun-labs/tree/main/hermes-agent-skills-and-memory)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `append-log.sh` | <a href="https://fankh.github.io/copyandrun-labs/hermes-agent-skills-and-memory/append-log.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/hermes-agent-skills-and-memory/append-log.sh) |
| `count_errors.py` | <a href="https://fankh.github.io/copyandrun-labs/hermes-agent-skills-and-memory/count_errors.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/hermes-agent-skills-and-memory/count_errors.py) |
| `docker-compose.yml` | <a href="https://fankh.github.io/copyandrun-labs/hermes-agent-skills-and-memory/docker-compose.yml" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/hermes-agent-skills-and-memory/docker-compose.yml) |
| `Dockerfile` | <a href="https://fankh.github.io/copyandrun-labs/hermes-agent-skills-and-memory/Dockerfile" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/hermes-agent-skills-and-memory/Dockerfile) |
| `find-secret.sh` | <a href="https://fankh.github.io/copyandrun-labs/hermes-agent-skills-and-memory/find-secret.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/hermes-agent-skills-and-memory/find-secret.sh) |
| `forget-session.sh` | <a href="https://fankh.github.io/copyandrun-labs/hermes-agent-skills-and-memory/forget-session.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/hermes-agent-skills-and-memory/forget-session.sh) |
| `seed-log.sh` | <a href="https://fankh.github.io/copyandrun-labs/hermes-agent-skills-and-memory/seed-log.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/hermes-agent-skills-and-memory/seed-log.sh) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
