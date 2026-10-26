#!/bin/bash
# Kibana 시간대를 UTC로 맞추고 web-access-sigma 데이터 뷰를 만듭니다.
K="${KIBANA:-http://127.0.0.1:19501}"
curl -s -X POST "$K/api/kibana/settings" \
  -H 'kbn-xsrf: true' -H 'Content-Type: application/json' \
  -d '{"changes":{"dateFormat:tz":"UTC"}}' >/dev/null
curl -s -X POST "$K/api/data_views/data_view" \
  -H 'kbn-xsrf: true' -H 'Content-Type: application/json' \
  -d '{"data_view":{"id":"web-access-sigma-dv","title":"web-access-sigma","name":"web-access-sigma","timeFieldName":"@timestamp"}}' \
  | grep -o '"id":"[^"]*"' | head -1
