# auth.log로 SSH 침입 흔적 읽기: 실패 반복, 성공 로그인, 직후 sudo를 시간순으로

컨테이너에 openssh-server와 rsyslog를 띄우고 ssh 명령 몇 번으로 실패 로그인 7번과 성공 로그인 1번을 만든 뒤, 실제 auth.log에서 실패 반복, 실패 뒤 첫 성공, 성공 세션의 sudo와 계정 생성 기록을 파이썬 스크립트로 시간순 타임라인으로 읽습니다. 키 인증 전환과 로그 보존 점검표도 함께 봅니다.

## 링크

- 글: [https://copyandrun.com/blog/linux-auth-log-ssh-intrusion-triage/](https://copyandrun.com/blog/linux-auth-log-ssh-intrusion-triage/)
- 한 번에 받기: [linux-auth-log-ssh-intrusion-triage.zip](https://copyandrun.com/code-zip/linux-auth-log-ssh-intrusion-triage.zip)
- GitHub 폴더: [copyandrun-labs/linux-auth-log-ssh-intrusion-triage](https://github.com/fankh/copyandrun-labs/tree/main/linux-auth-log-ssh-intrusion-triage)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `Dockerfile` | <a href="https://fankh.github.io/copyandrun-labs/linux-auth-log-ssh-intrusion-triage/Dockerfile" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/linux-auth-log-ssh-intrusion-triage/Dockerfile) |
| `harden.sh` | <a href="https://fankh.github.io/copyandrun-labs/linux-auth-log-ssh-intrusion-triage/harden.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/linux-auth-log-ssh-intrusion-triage/harden.sh) |
| `hardening.conf` | <a href="https://fankh.github.io/copyandrun-labs/linux-auth-log-ssh-intrusion-triage/hardening.conf" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/linux-auth-log-ssh-intrusion-triage/hardening.conf) |
| `make_logs.sh` | <a href="https://fankh.github.io/copyandrun-labs/linux-auth-log-ssh-intrusion-triage/make_logs.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/linux-auth-log-ssh-intrusion-triage/make_logs.sh) |
| `start.sh` | <a href="https://fankh.github.io/copyandrun-labs/linux-auth-log-ssh-intrusion-triage/start.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/linux-auth-log-ssh-intrusion-triage/start.sh) |
| `triage.py` | <a href="https://fankh.github.io/copyandrun-labs/linux-auth-log-ssh-intrusion-triage/triage.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/linux-auth-log-ssh-intrusion-triage/triage.py) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
