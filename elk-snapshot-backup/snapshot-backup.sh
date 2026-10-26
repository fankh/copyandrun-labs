#!/bin/bash
# 저장소 등록
curl -s -X PUT "http://127.0.0.1:9200/_snapshot/backup" \
  -H 'Content-Type: application/json' \
  -d '{"type":"fs","settings":{"location":"/var/lib/elasticsearch/snapshots"}}'

# 스냅샷 저장
curl -s -X PUT "http://127.0.0.1:9200/_snapshot/backup/installed?wait_for_completion=true" \
  -o /dev/null -w "snapshot: %{http_code}\n"

# 저장된 스냅샷 확인
curl -s "http://127.0.0.1:9200/_cat/snapshots/backup?v&h=id,status,indices,successful_shards"
