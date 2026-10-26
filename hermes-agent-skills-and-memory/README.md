# Hermes Agent의 스킬과 메모리, 저장되는 정보 확인하기

세션을 닫고 새로 열어도 메모리가 남는지, 에이전트가 만든 스킬을 슬래시 명령으로 다시 쓸 수 있는지 확인하고, ~/.hermes 안에 대화와 입력 기록이 어디에 남는지 찾아 가짜 토큰 문자열로 저장 위험과 정리 방법을 점검합니다.

글: https://copyandrun.com/blog/hermes-agent-skills-and-memory/

## 파일

- `append-log.sh`
- `count_errors.py`
- `docker-compose.yml`
- `Dockerfile`
- `find-secret.sh`
- `forget-session.sh`
- `seed-log.sh`

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
