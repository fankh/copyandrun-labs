# Hermes Agent를 호스트가 아닌 Docker 컨테이너에 설치하고 첫 실행하기

명령을 직접 실행하는 오픈소스 에이전트 Hermes Agent를 Ubuntu 컨테이너 안에 설치 스크립트로 설치하고, 첫 실행 화면, hermes doctor 점검, ~/.hermes 데이터 폴더 구조, 웹 대시보드 로그인까지 직접 확인합니다.

글: https://copyandrun.com/blog/hermes-agent-install-in-docker/

## 파일

- `docker-compose.yml`
- `Dockerfile`

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
