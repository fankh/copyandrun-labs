# testssl.sh로 내 서버의 TLS 설정 점검하기: 약한 서버와 고친 서버를 같은 기준으로 비교

일부러 약하게 만든 nginx와 고친 nginx를 컨테이너로 띄워 testssl.sh로 점검합니다. 프로토콜, 인증서, 취약점, 보안 헤더를 읽고, JSON 결과를 심각도로 집계해 CI 기준(종료 코드)까지 만들어 실행으로 확인합니다.

글: https://copyandrun.com/blog/testssl-local-tls-check/

## 파일

- `nginx_bad.conf`
- `nginx_good.conf`
- `testssl_demo.sh`
- `testssl_summary.py`

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
