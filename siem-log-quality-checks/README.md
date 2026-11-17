# SIEM에 들어온 로그가 믿을 만한지 점검하기: 유실, 중복, 시간 어긋남

샘플 로그를 직접 만들어 유실, 중복, 파싱 실패, 시간 어긋남을 Python 스크립트로 찾아냅니다. 점검 결과를 어떤 기준으로 읽는지도 함께 정리합니다.

## 링크

- 글: [https://copyandrun.com/blog/siem-log-quality-checks/](https://copyandrun.com/blog/siem-log-quality-checks/)
- 한 번에 받기: [siem-log-quality-checks.zip](https://copyandrun.com/code-zip/siem-log-quality-checks.zip)
- GitHub 폴더: [copyandrun-labs/siem-log-quality-checks](https://github.com/fankh/copyandrun-labs/tree/main/siem-log-quality-checks)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `check_quality.py` | <a href="https://fankh.github.io/copyandrun-labs/siem-log-quality-checks/check_quality.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/siem-log-quality-checks/check_quality.py) |
| `make_sample.py` | <a href="https://fankh.github.io/copyandrun-labs/siem-log-quality-checks/make_sample.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/siem-log-quality-checks/make_sample.py) |
| `report.py` | <a href="https://fankh.github.io/copyandrun-labs/siem-log-quality-checks/report.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/siem-log-quality-checks/report.py) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
