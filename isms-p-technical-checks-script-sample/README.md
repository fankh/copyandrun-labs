# ISMS-P 기술 점검 항목 일부를 스크립트로 확인해 양호, 취약, 수동확인 표 만들기

일부러 허술하게 만든 nginx 시험 서버에서 계정 관리, 접근 로그의 권한과 보관 기간, TLS 버전, 저장 데이터 암호화를 파이썬 스크립트로 점검해 표를 만들고, 설정을 고친 뒤 취약 8건이 양호로 바뀌는 것을 확인합니다. 참고용 자동 점검이며 인증 심사를 대신하지 않습니다.

## 링크

- 글: [https://copyandrun.com/blog/isms-p-technical-checks-script-sample/](https://copyandrun.com/blog/isms-p-technical-checks-script-sample/)
- 한 번에 받기: [isms-p-technical-checks-script-sample.zip](https://copyandrun.com/code-zip/isms-p-technical-checks-script-sample.zip)
- GitHub 폴더: [copyandrun-labs/isms-p-technical-checks-script-sample](https://github.com/fankh/copyandrun-labs/tree/main/isms-p-technical-checks-script-sample)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `check.py` | <a href="https://fankh.github.io/copyandrun-labs/isms-p-technical-checks-script-sample/check.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/isms-p-technical-checks-script-sample/check.py) |
| `Dockerfile` | <a href="https://fankh.github.io/copyandrun-labs/isms-p-technical-checks-script-sample/Dockerfile" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/isms-p-technical-checks-script-sample/Dockerfile) |
| `fix.sh` | <a href="https://fankh.github.io/copyandrun-labs/isms-p-technical-checks-script-sample/fix.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/isms-p-technical-checks-script-sample/fix.sh) |
| `weak_setup.sh` | <a href="https://fankh.github.io/copyandrun-labs/isms-p-technical-checks-script-sample/weak_setup.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/isms-p-technical-checks-script-sample/weak_setup.sh) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
