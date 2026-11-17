# Caddy 리버스 프록시에 HTTPS와 기본 인증 걸기

인증이 없는 내부 웹 서비스 앞에 Caddy를 리버스 프록시로 세워 자체 HTTPS 인증서, 기본 인증, 보안 헤더, HTTP 리다이렉트를 설정하고 curl로 하나씩 확인합니다. 인증서가 왜 브라우저에서 경고를 내는지, 뒤쪽 앱이 바깥에 열리지 않는지까지 실행해 봅니다.

## 링크

- 글: [https://copyandrun.com/blog/caddy-reverse-proxy-basic-auth-https/](https://copyandrun.com/blog/caddy-reverse-proxy-basic-auth-https/)
- 한 번에 받기: [caddy-reverse-proxy-basic-auth-https.zip](https://copyandrun.com/code-zip/caddy-reverse-proxy-basic-auth-https.zip)
- GitHub 폴더: [copyandrun-labs/caddy-reverse-proxy-basic-auth-https](https://github.com/fankh/copyandrun-labs/tree/main/caddy-reverse-proxy-basic-auth-https)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `caddy_demo.sh` | <a href="https://fankh.github.io/copyandrun-labs/caddy-reverse-proxy-basic-auth-https/caddy_demo.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/caddy-reverse-proxy-basic-auth-https/caddy_demo.sh) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
