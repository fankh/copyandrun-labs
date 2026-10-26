# 파이썬 비밀번호 해시와 하드코딩된 시크릿 정리하기

MD5로 저장하고 코드에 비밀번호가 박힌 회원 가입 예제를 Bandit으로 검사한 뒤, argon2-cffi 해시와 환경 변수 분리로 고쳐 다시 통과시킵니다. 해시 문자열 구조와 needs_rehash 재해시도 직접 확인합니다.

글: https://copyandrun.com/blog/python-password-hash-and-secrets/

## 파일

- `after_accounts.py`
- `before_accounts.py`
- `demo.py`
- `env.txt`
- `index.html`
- `rehash.py`
- `requirements.txt`
- `structure.py`
- `web.py`

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
