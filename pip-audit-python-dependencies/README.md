# pip-audit로 파이썬 의존성 취약점 점검하기: 고칠 버전과 종료 코드

일부러 오래된 버전을 적은 requirements.txt를 pip-audit로 점검해 18행의 결과를 읽습니다. 같은 항목이 두 번씩 나오는 이유를 고유 번호로 정리하고, 취약점이 있을 때 종료 코드 1, 없을 때 0이 나오는 것을 확인합니다.

## 링크

- 글: [https://copyandrun.com/blog/pip-audit-python-dependencies/](https://copyandrun.com/blog/pip-audit-python-dependencies/)
- 한 번에 받기: [pip-audit-python-dependencies.zip](https://copyandrun.com/code-zip/pip-audit-python-dependencies.zip)
- GitHub 폴더: [copyandrun-labs/pip-audit-python-dependencies](https://github.com/fankh/copyandrun-labs/tree/main/pip-audit-python-dependencies)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `audit.sh` | <a href="https://fankh.github.io/copyandrun-labs/pip-audit-python-dependencies/audit.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/pip-audit-python-dependencies/audit.sh) |
| `audit_more.sh` | <a href="https://fankh.github.io/copyandrun-labs/pip-audit-python-dependencies/audit_more.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/pip-audit-python-dependencies/audit_more.sh) |
| `requirements.txt` | <a href="https://fankh.github.io/copyandrun-labs/pip-audit-python-dependencies/requirements.txt" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/pip-audit-python-dependencies/requirements.txt) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
