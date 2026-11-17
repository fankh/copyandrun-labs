# 파이썬 비밀번호 해시와 하드코딩된 시크릿 정리하기

MD5로 저장하고 코드에 비밀번호가 박힌 회원 가입 예제를 Bandit으로 검사한 뒤, argon2-cffi 해시와 환경 변수 분리로 고쳐 다시 통과시킵니다. 해시 문자열 구조와 needs_rehash 재해시도 직접 확인합니다.

## 링크

- 글: [https://copyandrun.com/blog/python-password-hash-and-secrets/](https://copyandrun.com/blog/python-password-hash-and-secrets/)
- 한 번에 받기: [python-password-hash-and-secrets.zip](https://copyandrun.com/code-zip/python-password-hash-and-secrets.zip)
- GitHub 폴더: [copyandrun-labs/python-password-hash-and-secrets](https://github.com/fankh/copyandrun-labs/tree/main/python-password-hash-and-secrets)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `after_accounts.py` | <a href="https://fankh.github.io/copyandrun-labs/python-password-hash-and-secrets/after_accounts.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/python-password-hash-and-secrets/after_accounts.py) |
| `before_accounts.py` | <a href="https://fankh.github.io/copyandrun-labs/python-password-hash-and-secrets/before_accounts.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/python-password-hash-and-secrets/before_accounts.py) |
| `demo.py` | <a href="https://fankh.github.io/copyandrun-labs/python-password-hash-and-secrets/demo.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/python-password-hash-and-secrets/demo.py) |
| `env.txt` | <a href="https://fankh.github.io/copyandrun-labs/python-password-hash-and-secrets/env.txt" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/python-password-hash-and-secrets/env.txt) |
| `index.html` | <a href="https://fankh.github.io/copyandrun-labs/python-password-hash-and-secrets/index.html" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/python-password-hash-and-secrets/index.html) |
| `rehash.py` | <a href="https://fankh.github.io/copyandrun-labs/python-password-hash-and-secrets/rehash.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/python-password-hash-and-secrets/rehash.py) |
| `requirements.txt` | <a href="https://fankh.github.io/copyandrun-labs/python-password-hash-and-secrets/requirements.txt" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/python-password-hash-and-secrets/requirements.txt) |
| `structure.py` | <a href="https://fankh.github.io/copyandrun-labs/python-password-hash-and-secrets/structure.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/python-password-hash-and-secrets/structure.py) |
| `web.py` | <a href="https://fankh.github.io/copyandrun-labs/python-password-hash-and-secrets/web.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/python-password-hash-and-secrets/web.py) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
