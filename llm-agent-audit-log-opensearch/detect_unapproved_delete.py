"""규칙: delete_file 이 승인 번호 없이 호출되면 agent-alerts 에 경고 문서를 만듭니다."""
import json
import urllib.error
import urllib.request

OS = "http://127.0.0.1:5740"

QUERY = {
    "size": 100,
    "query": {"bool": {"filter": [
        {"term": {"tool": "delete_file"}},
        {"term": {"status": "ok"}},
        {"term": {"approval": "none"}},
    ]}},
}


def call(method, path, body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(OS + path, data, {"Content-Type": "application/json"}, method=method)
    return json.load(urllib.request.urlopen(req))


created = 0
for hit in call("POST", "/agent-audit/_search", QUERY)["hits"]["hits"]:
    d = hit["_source"]
    alert = {
        "@timestamp": d["@timestamp"],
        "rule": "unapproved-delete",
        "severity": "high",
        "agent_id": d["agent_id"],
        "session_id": d["session_id"],
        "run_id": d["run_id"],
        "tool": d["tool"],
        "args_summary": d["args_summary"],
        "audit_doc_id": hit["_id"],
    }
    try:  # 감사 문서 ID 를 경고 ID 로 써서 다시 실행해도 중복되지 않게 합니다
        call("PUT", f"/agent-alerts/_create/{hit['_id']}?refresh=true", alert)
        created += 1
    except urllib.error.HTTPError as exc:
        if exc.code != 409:
            raise
print(f"경고 {created}건 생성")
