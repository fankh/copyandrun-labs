# testssl.sh로 내 서버의 TLS 설정 점검하기: 약한 서버와 고친 서버를 같은 기준으로 비교

일부러 약하게 만든 nginx와 고친 nginx를 컨테이너로 띄워 testssl.sh로 점검합니다. 프로토콜, 인증서, 취약점, 보안 헤더를 읽고, JSON 결과를 심각도로 집계해 CI 기준(종료 코드)까지 만들어 실행으로 확인합니다.

## 링크

- 글: [https://copyandrun.com/blog/testssl-local-tls-check/](https://copyandrun.com/blog/testssl-local-tls-check/)
- 한 번에 받기: [testssl-local-tls-check.zip](https://copyandrun.com/code-zip/testssl-local-tls-check.zip)
- GitHub 폴더: [copyandrun-labs/testssl-local-tls-check](https://github.com/fankh/copyandrun-labs/tree/main/testssl-local-tls-check)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `nginx_bad.conf` | <a href="https://fankh.github.io/copyandrun-labs/testssl-local-tls-check/nginx_bad.conf" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/testssl-local-tls-check/nginx_bad.conf) |
| `nginx_good.conf` | <a href="https://fankh.github.io/copyandrun-labs/testssl-local-tls-check/nginx_good.conf" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/testssl-local-tls-check/nginx_good.conf) |
| `testssl_demo.sh` | <a href="https://fankh.github.io/copyandrun-labs/testssl-local-tls-check/testssl_demo.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/testssl-local-tls-check/testssl_demo.sh) |
| `testssl_summary.py` | <a href="https://fankh.github.io/copyandrun-labs/testssl-local-tls-check/testssl_summary.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/testssl-local-tls-check/testssl_summary.py) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
