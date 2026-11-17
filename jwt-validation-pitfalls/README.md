# JWT 검증 실수: 서명 확인 끄기, alg none, 알고리즘 혼동, 만료와 aud

정상 토큰 1개와 공격 토큰 6개(alg none, 다른 키 서명, 만료, 다른 aud, 본문 변조, HS256 혼동)를 서명 확인을 끈 검증기, 헤더의 알고리즘을 믿는 검증기, 고친 검증기에 넣어 수락과 거절을 비교합니다. PyJWT가 막아 주는 것과 못 막는 것을 가르고 Node 구현으로 교차 확인합니다.

## 링크

- 글: [https://copyandrun.com/blog/jwt-validation-pitfalls/](https://copyandrun.com/blog/jwt-validation-pitfalls/)
- 한 번에 받기: [jwt-validation-pitfalls.zip](https://copyandrun.com/code-zip/jwt-validation-pitfalls.zip)
- GitHub 폴더: [copyandrun-labs/jwt-validation-pitfalls](https://github.com/fankh/copyandrun-labs/tree/main/jwt-validation-pitfalls)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `jwt_demo.sh` | <a href="https://fankh.github.io/copyandrun-labs/jwt-validation-pitfalls/jwt_demo.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/jwt-validation-pitfalls/jwt_demo.sh) |
| `make_tokens.py` | <a href="https://fankh.github.io/copyandrun-labs/jwt-validation-pitfalls/make_tokens.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/jwt-validation-pitfalls/make_tokens.py) |
| `node_verify.js` | <a href="https://fankh.github.io/copyandrun-labs/jwt-validation-pitfalls/node_verify.js" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/jwt-validation-pitfalls/node_verify.js) |
| `run_all.py` | <a href="https://fankh.github.io/copyandrun-labs/jwt-validation-pitfalls/run_all.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/jwt-validation-pitfalls/run_all.py) |
| `verifier_bad.py` | <a href="https://fankh.github.io/copyandrun-labs/jwt-validation-pitfalls/verifier_bad.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/jwt-validation-pitfalls/verifier_bad.py) |
| `verifier_good.py` | <a href="https://fankh.github.io/copyandrun-labs/jwt-validation-pitfalls/verifier_good.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/jwt-validation-pitfalls/verifier_good.py) |
| `verifier_nosig.py` | <a href="https://fankh.github.io/copyandrun-labs/jwt-validation-pitfalls/verifier_nosig.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/jwt-validation-pitfalls/verifier_nosig.py) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
