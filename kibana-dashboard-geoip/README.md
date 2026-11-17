# Kibana 대시보드와 GeoIP 지도로 접속 현황 보기

Docker compose로 Elasticsearch 8.19와 Kibana 8.19를 띄우고, ingest pipeline의 geoip 프로세서로 접근 로그의 IP에 위치 정보를 붙입니다. 상위 IP, 상태 코드, 시간대별 요청 수, 지도 패널을 대시보드로 저장하고 저장 객체를 내보내 다시 가져옵니다.

## 링크

- 글: [https://copyandrun.com/blog/kibana-dashboard-geoip/](https://copyandrun.com/blog/kibana-dashboard-geoip/)
- 한 번에 받기: [kibana-dashboard-geoip.zip](https://copyandrun.com/code-zip/kibana-dashboard-geoip.zip)
- GitHub 폴더: [copyandrun-labs/kibana-dashboard-geoip](https://github.com/fankh/copyandrun-labs/tree/main/kibana-dashboard-geoip)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `access-dashboard-import.ndjson` | <a href="https://fankh.github.io/copyandrun-labs/kibana-dashboard-geoip/access-dashboard-import.ndjson" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/kibana-dashboard-geoip/access-dashboard-import.ndjson) |
| `compose.yml` | <a href="https://fankh.github.io/copyandrun-labs/kibana-dashboard-geoip/compose.yml" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/kibana-dashboard-geoip/compose.yml) |
| `delete-objects.json` | <a href="https://fankh.github.io/copyandrun-labs/kibana-dashboard-geoip/delete-objects.json" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/kibana-dashboard-geoip/delete-objects.json) |
| `make-logs.sh` | <a href="https://fankh.github.io/copyandrun-labs/kibana-dashboard-geoip/make-logs.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/kibana-dashboard-geoip/make-logs.sh) |
| `pipeline.json` | <a href="https://fankh.github.io/copyandrun-labs/kibana-dashboard-geoip/pipeline.json" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/kibana-dashboard-geoip/pipeline.json) |
| `q.json` | <a href="https://fankh.github.io/copyandrun-labs/kibana-dashboard-geoip/q.json" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/kibana-dashboard-geoip/q.json) |
| `show.py` | <a href="https://fankh.github.io/copyandrun-labs/kibana-dashboard-geoip/show.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/kibana-dashboard-geoip/show.py) |
| `template.json` | <a href="https://fankh.github.io/copyandrun-labs/kibana-dashboard-geoip/template.json" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/kibana-dashboard-geoip/template.json) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
