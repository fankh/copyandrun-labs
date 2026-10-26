# Docker로 ELK 실습 서버 준비하기

빈 리눅스 컨테이너를 띄우고, 그 안에 ELK를 직접 설치할 준비를 합니다. 메모리와 포트 요구사항, 매일 시작과 종료 방법, 자주 겪는 문제도 함께 다룹니다.

글: https://copyandrun.com/blog/elk-lab-server-docker/

## 파일

- `docker-compose.yml`
- `Dockerfile`
- `start-elk.sh`

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
