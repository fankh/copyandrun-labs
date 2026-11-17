# ssh-audit으로 sshd 암호 설정 점검하기: 약한 설정과 하드닝 설정 비교

OpenSSH 9.6 서버 컨테이너 두 개를 약한 알고리즘 설정과 하드닝 설정으로 띄우고 ssh-audit 3.9.0으로 점검해 fail과 warn 개수를 비교합니다. 실제 ssh 클라이언트로 같은 알고리즘을 강제해 협상이 거절되는지 대조하고, fail 개수를 종료 코드로 바꿉니다.

## 링크

- 글: [https://copyandrun.com/blog/ssh-audit-sshd-hardening/](https://copyandrun.com/blog/ssh-audit-sshd-hardening/)
- 한 번에 받기: [ssh-audit-sshd-hardening.zip](https://copyandrun.com/code-zip/ssh-audit-sshd-hardening.zip)
- GitHub 폴더: [copyandrun-labs/ssh-audit-sshd-hardening](https://github.com/fankh/copyandrun-labs/tree/main/ssh-audit-sshd-hardening)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `ssh_demo.sh` | <a href="https://fankh.github.io/copyandrun-labs/ssh-audit-sshd-hardening/ssh_demo.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/ssh-audit-sshd-hardening/ssh_demo.sh) |
| `ssh_summary.py` | <a href="https://fankh.github.io/copyandrun-labs/ssh-audit-sshd-hardening/ssh_summary.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/ssh-audit-sshd-hardening/ssh_summary.py) |
| `sshd_hardened.conf` | <a href="https://fankh.github.io/copyandrun-labs/ssh-audit-sshd-hardening/sshd_hardened.conf" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/ssh-audit-sshd-hardening/sshd_hardened.conf) |
| `sshd_weak.conf` | <a href="https://fankh.github.io/copyandrun-labs/ssh-audit-sshd-hardening/sshd_weak.conf" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/ssh-audit-sshd-hardening/sshd_weak.conf) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
