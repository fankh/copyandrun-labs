# Postfix와 OpenDKIM으로 DKIM 서명하고 검증하기

외부로 나가지 못하는 전용 Docker 네트워크에 보내는 서버, 받는 서버, 시험 DNS를 만들고, opendkim-genkey로 만든 키로 메일 1통에 DKIM-Signature를 붙여 받는 쪽 Authentication-Results에서 dkim=pass를 확인합니다. 본문 1바이트를 바꾸면 dkim=fail이 되는 것도 해시 값으로 대조하고, 선택자와 키 교체 방법을 정리합니다.

글: https://copyandrun.com/blog/postfix-opendkim-sign-verify-local/

## 파일

- `bodyhash.py`
- `dns.conf`
- `Dockerfile`
- `entrypoint.sh`
- `headers.py`
- `mkdns.py`
- `recv-main.cf`
- `send-main.cf`
- `send_mail.sh`
- `setup.sh`
- `sign.conf`
- `tamper.py`
- `verify.conf`

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
