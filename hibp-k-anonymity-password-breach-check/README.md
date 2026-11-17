# Pwned Passwords 확인: Have I Been Pwned k-익명성 API 조회

Have I Been Pwned의 range API는 비밀번호도 전체 해시도 보내지 않고 SHA-1 앞 5자리만 보냅니다. 파이썬 스크립트로 해시 계산, 앞 5자리 조회, 나머지 35자리 로컬 대조, 일치 횟수 출력까지 구현하고, Add-Padding 헤더와 이 방식의 한계를 실제 응답으로 확인합니다.

## 링크

- 글: [https://copyandrun.com/blog/hibp-k-anonymity-password-breach-check/](https://copyandrun.com/blog/hibp-k-anonymity-password-breach-check/)
- 한 번에 받기: [hibp-k-anonymity-password-breach-check.zip](https://copyandrun.com/code-zip/hibp-k-anonymity-password-breach-check.zip)
- GitHub 폴더: [copyandrun-labs/hibp-k-anonymity-password-breach-check](https://github.com/fankh/copyandrun-labs/tree/main/hibp-k-anonymity-password-breach-check)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `hibp_check.py` | <a href="https://fankh.github.io/copyandrun-labs/hibp-k-anonymity-password-breach-check/hibp_check.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/hibp-k-anonymity-password-breach-check/hibp_check.py) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
