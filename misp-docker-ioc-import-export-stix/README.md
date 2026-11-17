# MISP IOC 모으고 STIX 2.1로 내보내기: PyMISP

공식 misp-docker 구성으로 MISP를 띄우고 시험용 IOC 8건(example.com 도메인, 문서용 IP, 직접 만든 해시)을 CSV에서 PyMISP로 이벤트 하나에 넣습니다. 이벤트, 속성, 태그가 어떻게 묶이는지 웹 화면으로 보고, REST API로 JSON, CSV, STIX 2.1을 내려받아 indicator 패턴과 observed-data를 읽는 스크립트까지 돌려 봅니다.

글: https://copyandrun.com/blog/misp-docker-ioc-import-export-stix/

## 파일

- `docker-compose.override.yml`
- `export_stix.py`
- `import_iocs.py`
- `iocs.csv`
- `read_stix.py`
- `rest_calls.sh`
- `setup.sh`

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
