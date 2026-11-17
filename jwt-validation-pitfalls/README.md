# JWT 검증 실수: 서명 확인 끄기, alg none, 알고리즘 혼동, 만료와 aud

정상 토큰 1개와 공격 토큰 6개(alg none, 다른 키 서명, 만료, 다른 aud, 본문 변조, HS256 혼동)를 서명 확인을 끈 검증기, 헤더의 알고리즘을 믿는 검증기, 고친 검증기에 넣어 수락과 거절을 비교합니다. PyJWT가 막아 주는 것과 못 막는 것을 가르고 Node 구현으로 교차 확인합니다.

글: https://copyandrun.com/blog/jwt-validation-pitfalls/

## 파일

- `jwt_demo.sh`
- `make_tokens.py`
- `node_verify.js`
- `run_all.py`
- `verifier_bad.py`
- `verifier_good.py`
- `verifier_nosig.py`

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
