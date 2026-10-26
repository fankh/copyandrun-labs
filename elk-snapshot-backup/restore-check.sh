#!/bin/bash
# 1) 복원 전 상태
curl -s "http://127.0.0.1:9200/_cat/indices/logs-*?h=index,docs.count&s=index"

# 2) 인덱스 하나를 일부러 지웁니다
curl -s -X DELETE "http://127.0.0.1:9200/logs-auth"; echo
curl -s "http://127.0.0.1:9200/_cat/indices/logs-*?h=index,docs.count&s=index"

# 3) 스냅샷에서 그 인덱스만 복원합니다
curl -s -X POST "http://127.0.0.1:9200/_snapshot/backup/installed/_restore?wait_for_completion=true" \
  -H 'Content-Type: application/json' \
  -d '{"indices":"logs-auth","include_global_state":false}'; echo

# 4) 복원 후 문서 수가 같은지 확인합니다
curl -s "http://127.0.0.1:9200/_cat/indices/logs-*?h=index,docs.count&s=index"
