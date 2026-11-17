# Ubuntu SSH 서버 설정 점검: sshd -T로 유효 설정을 확인하고 암호 로그인을 끄는 방법

Ubuntu Server 22.04의 sshd가 실제로 쓰는 설정을 sshd -T로 읽어 권고값과 비교하는 스크립트를 만듭니다. 드롭인 파일 이름이 99로 시작하면 cloud-init 설정에 밀려 암호 로그인이 꺼지지 않는 함정을 화면으로 재현하고, 00으로 바꿔 해결한 뒤 암호 로그인이 거부되는 것까지 확인합니다.

## 링크

- 글: [https://copyandrun.com/blog/ssh-server-hardening-ubuntu-sshd-config/](https://copyandrun.com/blog/ssh-server-hardening-ubuntu-sshd-config/)
- 한 번에 받기: [ssh-server-hardening-ubuntu-sshd-config.zip](https://copyandrun.com/code-zip/ssh-server-hardening-ubuntu-sshd-config.zip)
- GitHub 폴더: [copyandrun-labs/ssh-server-hardening-ubuntu-sshd-config](https://github.com/fankh/copyandrun-labs/tree/main/ssh-server-hardening-ubuntu-sshd-config)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `ssh-hardening.conf` | <a href="https://fankh.github.io/copyandrun-labs/ssh-server-hardening-ubuntu-sshd-config/ssh-hardening.conf" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/ssh-server-hardening-ubuntu-sshd-config/ssh-hardening.conf) |
| `sshd-audit.sh` | <a href="https://fankh.github.io/copyandrun-labs/ssh-server-hardening-ubuntu-sshd-config/sshd-audit.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/ssh-server-hardening-ubuntu-sshd-config/sshd-audit.sh) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
