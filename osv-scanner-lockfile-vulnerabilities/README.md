# OSV-Scanner로 잠금 파일 점검하기: 34건을 읽고, 예외를 두고, 0건이 될 때까지 고치기

오래된 버전을 일부러 적은 requirements.txt와 package-lock.json을 OSV-Scanner에 넣어 취약점 34건을 찾습니다. JSON 요약, 예외 설정, 고친 뒤에도 남는 하위 의존성 두 건을 거쳐 종료 코드 0이 되기까지 실행해 확인합니다.

## 링크

- 글: [https://copyandrun.com/blog/osv-scanner-lockfile-vulnerabilities/](https://copyandrun.com/blog/osv-scanner-lockfile-vulnerabilities/)
- 한 번에 받기: [osv-scanner-lockfile-vulnerabilities.zip](https://copyandrun.com/code-zip/osv-scanner-lockfile-vulnerabilities.zip)
- GitHub 폴더: [copyandrun-labs/osv-scanner-lockfile-vulnerabilities](https://github.com/fankh/copyandrun-labs/tree/main/osv-scanner-lockfile-vulnerabilities)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `osv_demo.sh` | <a href="https://fankh.github.io/copyandrun-labs/osv-scanner-lockfile-vulnerabilities/osv_demo.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/osv-scanner-lockfile-vulnerabilities/osv_demo.sh) |
| `osv_summary.py` | <a href="https://fankh.github.io/copyandrun-labs/osv-scanner-lockfile-vulnerabilities/osv_summary.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/osv-scanner-lockfile-vulnerabilities/osv_summary.py) |
| `package-lock.json` | <a href="https://fankh.github.io/copyandrun-labs/osv-scanner-lockfile-vulnerabilities/package-lock.json" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/osv-scanner-lockfile-vulnerabilities/package-lock.json) |
| `requirements.txt` | <a href="https://fankh.github.io/copyandrun-labs/osv-scanner-lockfile-vulnerabilities/requirements.txt" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/osv-scanner-lockfile-vulnerabilities/requirements.txt) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
