# pip-audit로 파이썬 의존성 취약점 점검하기: 고칠 버전과 종료 코드

일부러 오래된 버전을 적은 requirements.txt를 pip-audit로 점검해 18행의 결과를 읽습니다. 같은 항목이 두 번씩 나오는 이유를 고유 번호로 정리하고, 취약점이 있을 때 종료 코드 1, 없을 때 0이 나오는 것을 확인합니다.

글: https://copyandrun.com/blog/pip-audit-python-dependencies/

## 파일

- `audit.sh`
- `audit_more.sh`
- `requirements.txt`

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
