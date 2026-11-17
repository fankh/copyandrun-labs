# Pwned Passwords 확인: Have I Been Pwned k-익명성 API 조회

Have I Been Pwned의 range API는 비밀번호도 전체 해시도 보내지 않고 SHA-1 앞 5자리만 보냅니다. 파이썬 스크립트로 해시 계산, 앞 5자리 조회, 나머지 35자리 로컬 대조, 일치 횟수 출력까지 구현하고, Add-Padding 헤더와 이 방식의 한계를 실제 응답으로 확인합니다.

글: https://copyandrun.com/blog/hibp-k-anonymity-password-breach-check/

## 파일

- `hibp_check.py`

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
