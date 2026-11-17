# OWASP ZAP baseline 스캔으로 내 앱을 점검하고 보고서 읽기

직접 만든 Flask 앱을 컨테이너로 띄우고 ZAP baseline 스캔을 돌려 결과 요약과 HTML 보고서를 읽습니다. 경고별로 보안 헤더와 쿠키 속성을 고친 뒤 다시 스캔하고, 규칙 설정 파일과 종료 코드로 CI 게이트를 만듭니다.

## 링크

- 글: [https://copyandrun.com/blog/zap-baseline-scan-own-app/](https://copyandrun.com/blog/zap-baseline-scan-own-app/)
- 한 번에 받기: [zap-baseline-scan-own-app.zip](https://copyandrun.com/code-zip/zap-baseline-scan-own-app.zip)
- GitHub 폴더: [copyandrun-labs/zap-baseline-scan-own-app](https://github.com/fankh/copyandrun-labs/tree/main/zap-baseline-scan-own-app)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `app-v2.py` | <a href="https://fankh.github.io/copyandrun-labs/zap-baseline-scan-own-app/app-v2.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/zap-baseline-scan-own-app/app-v2.py) |
| `app.py` | <a href="https://fankh.github.io/copyandrun-labs/zap-baseline-scan-own-app/app.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/zap-baseline-scan-own-app/app.py) |
| `Dockerfile` | <a href="https://fankh.github.io/copyandrun-labs/zap-baseline-scan-own-app/Dockerfile" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/zap-baseline-scan-own-app/Dockerfile) |
| `requirements.txt` | <a href="https://fankh.github.io/copyandrun-labs/zap-baseline-scan-own-app/requirements.txt" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/zap-baseline-scan-own-app/requirements.txt) |
| `zap-rules.tsv` | <a href="https://fankh.github.io/copyandrun-labs/zap-baseline-scan-own-app/zap-rules.tsv" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/zap-baseline-scan-own-app/zap-rules.tsv) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
