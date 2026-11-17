# ssh-audit으로 sshd 암호 설정 점검하기: 약한 설정과 하드닝 설정 비교

OpenSSH 9.6 서버 컨테이너 두 개를 약한 알고리즘 설정과 하드닝 설정으로 띄우고 ssh-audit 3.9.0으로 점검해 fail과 warn 개수를 비교합니다. 실제 ssh 클라이언트로 같은 알고리즘을 강제해 협상이 거절되는지 대조하고, fail 개수를 종료 코드로 바꿉니다.

글: https://copyandrun.com/blog/ssh-audit-sshd-hardening/

## 파일

- `ssh_demo.sh`
- `ssh_summary.py`
- `sshd_hardened.conf`
- `sshd_weak.conf`

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
