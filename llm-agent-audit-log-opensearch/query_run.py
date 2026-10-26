"""run_id 하나의 호출을 순서대로 다시 구성해 출력합니다."""
import json
import sys
import urllib.request

OS = "http://127.0.0.1:5740"
run_id = sys.argv[1]
query = {"size": 50, "sort": [{"@timestamp": "asc"}], "query": {"term": {"run_id": run_id}}}
req = urllib.request.Request(f"{OS}/agent-audit/_search", json.dumps(query).encode(), {"Content-Type": "application/json"})
for hit in json.load(urllib.request.urlopen(req))["hits"]["hits"]:
    d = hit["_source"]
    print(f'{d["seq"]}. {d["agent_id"]} {d["tool"]:12} {d["status"]:5} approval={d["approval"]:8} {d["args_summary"]}')
