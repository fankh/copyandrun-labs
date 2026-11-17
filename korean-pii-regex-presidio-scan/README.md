# 한국어 개인정보 찾기: 정규식과 Presidio 비교, 스캔 결과와 마스킹

주민등록번호 형식, 휴대전화 번호, 이메일, 사업자등록번호, 카드 번호를 직접 만든 가짜 파일 3개에서 찾습니다. 형식만 보는 정규식, 검증 로직을 붙인 정규식, Presidio 기본, Presidio에 한국어 recognizer를 더한 방식을 같은 정답표로 채점해 탐지, 오탐, 미탐을 표로 비교하고 앞 6자리만 남기는 마스킹까지 해 봅니다.

## 링크

- 글: [https://copyandrun.com/blog/korean-pii-regex-presidio-scan/](https://copyandrun.com/blog/korean-pii-regex-presidio-scan/)
- 한 번에 받기: [korean-pii-regex-presidio-scan.zip](https://copyandrun.com/code-zip/korean-pii-regex-presidio-scan.zip)
- GitHub 폴더: [copyandrun-labs/korean-pii-regex-presidio-scan](https://github.com/fankh/copyandrun-labs/tree/main/korean-pii-regex-presidio-scan)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `compare.py` | <a href="https://fankh.github.io/copyandrun-labs/korean-pii-regex-presidio-scan/compare.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/korean-pii-regex-presidio-scan/compare.py) |
| `Dockerfile` | <a href="https://fankh.github.io/copyandrun-labs/korean-pii-regex-presidio-scan/Dockerfile" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/korean-pii-regex-presidio-scan/Dockerfile) |
| `make_data.py` | <a href="https://fankh.github.io/copyandrun-labs/korean-pii-regex-presidio-scan/make_data.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/korean-pii-regex-presidio-scan/make_data.py) |
| `scan_presidio.py` | <a href="https://fankh.github.io/copyandrun-labs/korean-pii-regex-presidio-scan/scan_presidio.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/korean-pii-regex-presidio-scan/scan_presidio.py) |
| `scan_regex.py` | <a href="https://fankh.github.io/copyandrun-labs/korean-pii-regex-presidio-scan/scan_regex.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/korean-pii-regex-presidio-scan/scan_regex.py) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
