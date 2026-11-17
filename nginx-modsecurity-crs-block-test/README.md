# nginx ModSecurity와 OWASP CRS 웹 공격 차단 시험

ModSecurity 3과 OWASP 핵심 규칙 세트(CRS)가 든 nginx 컨테이너에 공격 요청 8건과 정상 요청 8건을 보내, 탐지만 하는 모드와 차단 모드, 민감도 1에서 4까지의 결과를 표로 비교합니다. 차단률과 오차단을 종료 코드 게이트로 바꾸고 민감도를 올리면 정상 요청이 막히는 지점을 확인합니다.

## 링크

- 글: [https://copyandrun.com/blog/nginx-modsecurity-crs-block-test/](https://copyandrun.com/blog/nginx-modsecurity-crs-block-test/)
- 한 번에 받기: [nginx-modsecurity-crs-block-test.zip](https://copyandrun.com/code-zip/nginx-modsecurity-crs-block-test.zip)
- GitHub 폴더: [copyandrun-labs/nginx-modsecurity-crs-block-test](https://github.com/fankh/copyandrun-labs/tree/main/nginx-modsecurity-crs-block-test)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `backend.conf` | <a href="https://fankh.github.io/copyandrun-labs/nginx-modsecurity-crs-block-test/backend.conf" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/nginx-modsecurity-crs-block-test/backend.conf) |
| `modsec_demo.sh` | <a href="https://fankh.github.io/copyandrun-labs/nginx-modsecurity-crs-block-test/modsec_demo.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/nginx-modsecurity-crs-block-test/modsec_demo.sh) |
| `modsec_matrix.py` | <a href="https://fankh.github.io/copyandrun-labs/nginx-modsecurity-crs-block-test/modsec_matrix.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/nginx-modsecurity-crs-block-test/modsec_matrix.py) |
| `modsec_summary.py` | <a href="https://fankh.github.io/copyandrun-labs/nginx-modsecurity-crs-block-test/modsec_summary.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/nginx-modsecurity-crs-block-test/modsec_summary.py) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
