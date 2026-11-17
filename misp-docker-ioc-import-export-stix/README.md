# MISP IOC 모으고 STIX 2.1로 내보내기: PyMISP

공식 misp-docker 구성으로 MISP를 띄우고 시험용 IOC 8건(example.com 도메인, 문서용 IP, 직접 만든 해시)을 CSV에서 PyMISP로 이벤트 하나에 넣습니다. 이벤트, 속성, 태그가 어떻게 묶이는지 웹 화면으로 보고, REST API로 JSON, CSV, STIX 2.1을 내려받아 indicator 패턴과 observed-data를 읽는 스크립트까지 돌려 봅니다.

## 링크

- 글: [https://copyandrun.com/blog/misp-docker-ioc-import-export-stix/](https://copyandrun.com/blog/misp-docker-ioc-import-export-stix/)
- 한 번에 받기: [misp-docker-ioc-import-export-stix.zip](https://copyandrun.com/code-zip/misp-docker-ioc-import-export-stix.zip)
- GitHub 폴더: [copyandrun-labs/misp-docker-ioc-import-export-stix](https://github.com/fankh/copyandrun-labs/tree/main/misp-docker-ioc-import-export-stix)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `docker-compose.override.yml` | <a href="https://fankh.github.io/copyandrun-labs/misp-docker-ioc-import-export-stix/docker-compose.override.yml" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/misp-docker-ioc-import-export-stix/docker-compose.override.yml) |
| `export_stix.py` | <a href="https://fankh.github.io/copyandrun-labs/misp-docker-ioc-import-export-stix/export_stix.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/misp-docker-ioc-import-export-stix/export_stix.py) |
| `import_iocs.py` | <a href="https://fankh.github.io/copyandrun-labs/misp-docker-ioc-import-export-stix/import_iocs.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/misp-docker-ioc-import-export-stix/import_iocs.py) |
| `iocs.csv` | <a href="https://fankh.github.io/copyandrun-labs/misp-docker-ioc-import-export-stix/iocs.csv" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/misp-docker-ioc-import-export-stix/iocs.csv) |
| `read_stix.py` | <a href="https://fankh.github.io/copyandrun-labs/misp-docker-ioc-import-export-stix/read_stix.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/misp-docker-ioc-import-export-stix/read_stix.py) |
| `rest_calls.sh` | <a href="https://fankh.github.io/copyandrun-labs/misp-docker-ioc-import-export-stix/rest_calls.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/misp-docker-ioc-import-export-stix/rest_calls.sh) |
| `setup.sh` | <a href="https://fankh.github.io/copyandrun-labs/misp-docker-ioc-import-export-stix/setup.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/misp-docker-ioc-import-export-stix/setup.sh) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
