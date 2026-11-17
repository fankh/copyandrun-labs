# Docker로 ELK 실습 서버 준비하기

빈 리눅스 컨테이너를 띄우고, 그 안에 ELK를 직접 설치할 준비를 합니다. 메모리와 포트 요구사항, 매일 시작과 종료 방법, 자주 겪는 문제도 함께 다룹니다.

## 링크

- 글: [https://copyandrun.com/blog/elk-lab-server-docker/](https://copyandrun.com/blog/elk-lab-server-docker/)
- 한 번에 받기: [elk-lab-server-docker.zip](https://copyandrun.com/code-zip/elk-lab-server-docker.zip)
- GitHub 폴더: [copyandrun-labs/elk-lab-server-docker](https://github.com/fankh/copyandrun-labs/tree/main/elk-lab-server-docker)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `docker-compose.yml` | <a href="https://fankh.github.io/copyandrun-labs/elk-lab-server-docker/docker-compose.yml" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/elk-lab-server-docker/docker-compose.yml) |
| `Dockerfile` | <a href="https://fankh.github.io/copyandrun-labs/elk-lab-server-docker/Dockerfile" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/elk-lab-server-docker/Dockerfile) |
| `start-elk.sh` | <a href="https://fankh.github.io/copyandrun-labs/elk-lab-server-docker/start-elk.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/elk-lab-server-docker/start-elk.sh) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
