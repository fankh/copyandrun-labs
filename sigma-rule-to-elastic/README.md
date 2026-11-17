# Sigma 룰을 작성하고 Elasticsearch 쿼리로 변환해 탐지하기

웹 서버 접근 로그용 Sigma 룰 3개를 작성해 sigma-cli로 점검하고 Lucene 쿼리로 변환합니다. 직접 만든 pipeline으로 필드명을 ECS 이름으로 바꾼 뒤 Elasticsearch 8.19와 Kibana Discover에서 탐지되는지 확인하고, 오탐을 줄이는 조건을 더한 뒤 Kibana 규칙으로 저장합니다.

## 링크

- 글: [https://copyandrun.com/blog/sigma-rule-to-elastic/](https://copyandrun.com/blog/sigma-rule-to-elastic/)
- 한 번에 받기: [sigma-rule-to-elastic.zip](https://copyandrun.com/code-zip/sigma-rule-to-elastic.zip)
- GitHub 폴더: [copyandrun-labs/sigma-rule-to-elastic](https://github.com/fankh/copyandrun-labs/tree/main/sigma-rule-to-elastic)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `access.ndjson` | <a href="https://fankh.github.io/copyandrun-labs/sigma-rule-to-elastic/access.ndjson" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/sigma-rule-to-elastic/access.ndjson) |
| `compose.yml` | <a href="https://fankh.github.io/copyandrun-labs/sigma-rule-to-elastic/compose.yml" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/sigma-rule-to-elastic/compose.yml) |
| `kibana-setup.sh` | <a href="https://fankh.github.io/copyandrun-labs/sigma-rule-to-elastic/kibana-setup.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/sigma-rule-to-elastic/kibana-setup.sh) |
| `make-rule.py` | <a href="https://fankh.github.io/copyandrun-labs/sigma-rule-to-elastic/make-rule.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/sigma-rule-to-elastic/make-rule.py) |
| `mapping.json` | <a href="https://fankh.github.io/copyandrun-labs/sigma-rule-to-elastic/mapping.json" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/sigma-rule-to-elastic/mapping.json) |
| `web-ecs.yml` | <a href="https://fankh.github.io/copyandrun-labs/sigma-rule-to-elastic/web-ecs.yml" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/sigma-rule-to-elastic/web-ecs.yml) |
| `web_admin_path_probe.yml` | <a href="https://fankh.github.io/copyandrun-labs/sigma-rule-to-elastic/web_admin_path_probe.yml" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/sigma-rule-to-elastic/web_admin_path_probe.yml) |
| `web_path_traversal_success.yml` | <a href="https://fankh.github.io/copyandrun-labs/sigma-rule-to-elastic/web_path_traversal_success.yml" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/sigma-rule-to-elastic/web_path_traversal_success.yml) |
| `web_scanner_user_agent.yml` | <a href="https://fankh.github.io/copyandrun-labs/sigma-rule-to-elastic/web_scanner_user_agent.yml" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/sigma-rule-to-elastic/web_scanner_user_agent.yml) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
