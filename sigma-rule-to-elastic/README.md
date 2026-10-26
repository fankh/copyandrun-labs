# Sigma 룰을 작성하고 Elasticsearch 쿼리로 변환해 탐지하기

웹 서버 접근 로그용 Sigma 룰 3개를 작성해 sigma-cli로 점검하고 Lucene 쿼리로 변환합니다. 직접 만든 pipeline으로 필드명을 ECS 이름으로 바꾼 뒤 Elasticsearch 8.19와 Kibana Discover에서 탐지되는지 확인하고, 오탐을 줄이는 조건을 더한 뒤 Kibana 규칙으로 저장합니다.

글: https://copyandrun.com/blog/sigma-rule-to-elastic/

## 파일

- `access.ndjson`
- `compose.yml`
- `kibana-setup.sh`
- `make-rule.py`
- `mapping.json`
- `web-ecs.yml`
- `web_admin_path_probe.yml`
- `web_path_traversal_success.yml`
- `web_scanner_user_agent.yml`

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
