# conftest와 Rego로 docker-compose 정책 만들기

Rego로 docker-compose.yml 정책 여덟 개(privileged, host 네트워크, docker.sock 마운트, 이미지 태그, 평문 비밀번호, root 실행 등)를 직접 쓰고 conftest verify로 시험합니다. 약한 파일, 경고만 있는 파일, 고친 파일의 종료 코드를 비교하고 docker.sock이 왜 위험한지 컨테이너로 확인하며 정책을 일부러 깨서 시험이 잡는지도 봅니다.

글: https://copyandrun.com/blog/conftest-rego-compose-policy/

## 파일

- `compose.bad.yml`
- `compose.good.yml`
- `compose.rego`
- `compose.warn.yml`
- `compose_test.rego`
- `conftest_break.sh`
- `conftest_demo.sh`

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
