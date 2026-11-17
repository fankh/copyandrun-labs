# SPF 조회 10회 한도 점검: include와 DNS 조회 횟수 세기

SPF는 평가 중 DNS 조회가 10번을 넘으면 permerror로 실패합니다. include, a, mx 같은 항목이 중첩될 때 조회 횟수를 세는 규칙을 정리하고, 시험용 SPF 레코드 표에서 13회가 나오는 과정을 Python 스크립트로 확인합니다.

글: https://copyandrun.com/blog/spf-lookup-limit-10-count/

## 파일

- `spf_count.py`

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
