# Postfix와 OpenDKIM으로 DKIM 서명하고 검증하기

외부로 나가지 못하는 전용 Docker 네트워크에 보내는 서버, 받는 서버, 시험 DNS를 만들고, opendkim-genkey로 만든 키로 메일 1통에 DKIM-Signature를 붙여 받는 쪽 Authentication-Results에서 dkim=pass를 확인합니다. 본문 1바이트를 바꾸면 dkim=fail이 되는 것도 해시 값으로 대조하고, 선택자와 키 교체 방법을 정리합니다.

## 링크

- 글: [https://copyandrun.com/blog/postfix-opendkim-sign-verify-local/](https://copyandrun.com/blog/postfix-opendkim-sign-verify-local/)
- 한 번에 받기: [postfix-opendkim-sign-verify-local.zip](https://copyandrun.com/code-zip/postfix-opendkim-sign-verify-local.zip)
- GitHub 폴더: [copyandrun-labs/postfix-opendkim-sign-verify-local](https://github.com/fankh/copyandrun-labs/tree/main/postfix-opendkim-sign-verify-local)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `bodyhash.py` | <a href="https://fankh.github.io/copyandrun-labs/postfix-opendkim-sign-verify-local/bodyhash.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/postfix-opendkim-sign-verify-local/bodyhash.py) |
| `dns.conf` | <a href="https://fankh.github.io/copyandrun-labs/postfix-opendkim-sign-verify-local/dns.conf" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/postfix-opendkim-sign-verify-local/dns.conf) |
| `Dockerfile` | <a href="https://fankh.github.io/copyandrun-labs/postfix-opendkim-sign-verify-local/Dockerfile" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/postfix-opendkim-sign-verify-local/Dockerfile) |
| `entrypoint.sh` | <a href="https://fankh.github.io/copyandrun-labs/postfix-opendkim-sign-verify-local/entrypoint.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/postfix-opendkim-sign-verify-local/entrypoint.sh) |
| `headers.py` | <a href="https://fankh.github.io/copyandrun-labs/postfix-opendkim-sign-verify-local/headers.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/postfix-opendkim-sign-verify-local/headers.py) |
| `mkdns.py` | <a href="https://fankh.github.io/copyandrun-labs/postfix-opendkim-sign-verify-local/mkdns.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/postfix-opendkim-sign-verify-local/mkdns.py) |
| `recv-main.cf` | <a href="https://fankh.github.io/copyandrun-labs/postfix-opendkim-sign-verify-local/recv-main.cf" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/postfix-opendkim-sign-verify-local/recv-main.cf) |
| `send-main.cf` | <a href="https://fankh.github.io/copyandrun-labs/postfix-opendkim-sign-verify-local/send-main.cf" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/postfix-opendkim-sign-verify-local/send-main.cf) |
| `send_mail.sh` | <a href="https://fankh.github.io/copyandrun-labs/postfix-opendkim-sign-verify-local/send_mail.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/postfix-opendkim-sign-verify-local/send_mail.sh) |
| `setup.sh` | <a href="https://fankh.github.io/copyandrun-labs/postfix-opendkim-sign-verify-local/setup.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/postfix-opendkim-sign-verify-local/setup.sh) |
| `sign.conf` | <a href="https://fankh.github.io/copyandrun-labs/postfix-opendkim-sign-verify-local/sign.conf" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/postfix-opendkim-sign-verify-local/sign.conf) |
| `tamper.py` | <a href="https://fankh.github.io/copyandrun-labs/postfix-opendkim-sign-verify-local/tamper.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/postfix-opendkim-sign-verify-local/tamper.py) |
| `verify.conf` | <a href="https://fankh.github.io/copyandrun-labs/postfix-opendkim-sign-verify-local/verify.conf" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/postfix-opendkim-sign-verify-local/verify.conf) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
