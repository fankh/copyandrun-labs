# Keycloak 로컬 구성과 OIDC PKCE 로그인: 코드 가로채기 방어 확인

Docker로 Keycloak을 띄워 realm, client, 테스트 사용자를 구성하고, Flask 클라이언트가 Authorization Code와 PKCE로 로그인해 ID 토큰의 iss, aud, exp, nonce를 검증합니다. PKCE를 요구하지 않는 client에서는 가로챈 인가 코드가 토큰으로 교환되는 것을 재현하고, PKCE S256을 필수로 켜서 code_verifier 없는 교환이 거부되는 것을 확인합니다.

글: https://copyandrun.com/blog/keycloak-oidc-pkce-local-login/

## 파일

- `app.py`
- `attack.py`
- `docker-compose.yml`
- `realm-lab.json`
- `requirements.txt`

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
