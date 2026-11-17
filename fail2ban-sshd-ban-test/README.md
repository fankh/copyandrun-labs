# fail2ban SSH 무차별 대입 차단: 3번 실패 차단과 40초 뒤 해제 확인

sshd가 도는 컨테이너에 fail2ban 1.0.2를 올리고 다른 컨테이너에서 비밀번호를 3번 틀려 차단되는 과정을 확인합니다. 차단 뒤에는 올바른 비밀번호도 거절되는 것, 다른 컨테이너는 영향이 없는 것, iptables 규칙과 로그, 수동 해제와 시간이 지난 자동 해제, 컨테이너에서 로그가 안 남는 문제까지 다룹니다.

## 링크

- 글: [https://copyandrun.com/blog/fail2ban-sshd-ban-test/](https://copyandrun.com/blog/fail2ban-sshd-ban-test/)
- 한 번에 받기: [fail2ban-sshd-ban-test.zip](https://copyandrun.com/code-zip/fail2ban-sshd-ban-test.zip)
- GitHub 폴더: [copyandrun-labs/fail2ban-sshd-ban-test](https://github.com/fankh/copyandrun-labs/tree/main/fail2ban-sshd-ban-test)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `f2b_demo.sh` | <a href="https://fankh.github.io/copyandrun-labs/fail2ban-sshd-ban-test/f2b_demo.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/fail2ban-sshd-ban-test/f2b_demo.sh) |
| `jail.local` | <a href="https://fankh.github.io/copyandrun-labs/fail2ban-sshd-ban-test/jail.local" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/fail2ban-sshd-ban-test/jail.local) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
