# Kibana 대시보드와 GeoIP 지도로 접속 현황 보기

Docker compose로 Elasticsearch 8.19와 Kibana 8.19를 띄우고, ingest pipeline의 geoip 프로세서로 접근 로그의 IP에 위치 정보를 붙입니다. 상위 IP, 상태 코드, 시간대별 요청 수, 지도 패널을 대시보드로 저장하고 저장 객체를 내보내 다시 가져옵니다.

글: https://copyandrun.com/blog/kibana-dashboard-geoip/

## 파일

- `access-dashboard-import.ndjson`
- `compose.yml`
- `delete-objects.json`
- `make-logs.sh`
- `pipeline.json`
- `q.json`
- `show.py`
- `template.json`

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
