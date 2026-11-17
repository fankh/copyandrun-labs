# auth.log로 SSH 침입 흔적 읽기: 실패 반복, 성공 로그인, 직후 sudo를 시간순으로

컨테이너에 openssh-server와 rsyslog를 띄우고 ssh 명령 몇 번으로 실패 로그인 7번과 성공 로그인 1번을 만든 뒤, 실제 auth.log에서 실패 반복, 실패 뒤 첫 성공, 성공 세션의 sudo와 계정 생성 기록을 파이썬 스크립트로 시간순 타임라인으로 읽습니다. 키 인증 전환과 로그 보존 점검표도 함께 봅니다.

글: https://copyandrun.com/blog/linux-auth-log-ssh-intrusion-triage/

## 파일

- `Dockerfile`
- `harden.sh`
- `hardening.conf`
- `make_logs.sh`
- `start.sh`
- `triage.py`

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
