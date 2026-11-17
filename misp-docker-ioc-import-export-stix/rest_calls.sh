#!/bin/sh
# REST API 로 같은 이벤트를 JSON, CSV, STIX 2.1 로 내려받습니다. 사용법: sh rest_calls.sh <이벤트 번호>
URL=http://127.0.0.1:18060
KEY=CrC11LabKeyTestOnly0123456789abcdefghijk
H="-H Authorization:$KEY -H Accept:application/json -H Content-Type:application/json"

echo '--- 속성 검색(JSON), 탐지 대상만'
curl -s $H -X POST $URL/attributes/restSearch \
  -d "{\"returnFormat\":\"json\",\"eventid\":$1,\"to_ids\":1}" \
  | python -c "import sys,json;[print(a['type'],a['value']) for a in json.load(sys.stdin)['response']['Attribute']]"

echo '--- CSV 내보내기 첫 3줄'
curl -s $H -X POST $URL/attributes/restSearch -d "{\"returnFormat\":\"csv\",\"eventid\":$1}" | head -3 | cut -d, -f3-5

echo '--- STIX 2.1 내보내기 요약'
curl -s $H -X POST $URL/events/restSearch -d "{\"returnFormat\":\"stix2\",\"eventid\":$1}" \
  | python -c "import sys,json;b=json.load(sys.stdin);print(b['type'],len(b['objects']),'개 객체')"
