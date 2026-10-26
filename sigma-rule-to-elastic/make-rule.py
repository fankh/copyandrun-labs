import json
import sys

# 표준입력으로 받은 Lucene 쿼리를 Kibana 규칙(Elasticsearch query) 요청 본문으로 바꿉니다.
query = sys.stdin.read().strip()
rule = {
    "name": "Known Scanner Name In User Agent",
    "rule_type_id": ".es-query",
    "consumer": "stackAlerts",
    "schedule": {"interval": "5m"},
    "tags": ["sigma"],
    "enabled": True,
    "actions": [],
    "params": {
        "searchType": "searchSource",
        "timeWindowSize": 365,
        "timeWindowUnit": "d",
        "threshold": [0],
        "thresholdComparator": ">",
        "size": 100,
        "aggType": "count",
        "groupBy": "all",
        "excludeHitsFromPreviousRun": False,
        "searchConfiguration": {
            "query": {"query": query, "language": "lucene"},
            "index": "web-access-sigma-dv",
        },
    },
}
print(json.dumps(rule))
