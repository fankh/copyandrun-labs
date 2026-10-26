#!/bin/bash
# Dashboards 에 security-web 인덱스 패턴을 만듭니다. 화면에서 Dashboards Management 의 Index patterns 로 만드는 것과 같습니다.
curl -s -XPOST http://dashboards:5601/api/saved_objects/index-pattern/security-web \
  -H 'Content-Type: application/json' -H 'osd-xsrf: true' \
  -d '{"attributes":{"title":"security-web","timeFieldName":"@timestamp"}}' | jq -c '{id: .id, title: .attributes.title}'
