"""인덱스 템플릿을 넣고, Dashboards 에 인덱스 패턴·저장된 검색·시각화를 만듭니다."""
import json
import urllib.request

OS = "http://127.0.0.1:5740"
DASH = "http://127.0.0.1:5741"


def call(method, url, body=None, headers=None):
    data = json.dumps(body).encode() if body is not None else None
    h = {"Content-Type": "application/json", "osd-xsrf": "true"}
    h.update(headers or {})
    req = urllib.request.Request(url, data, h, method=method)
    return json.load(urllib.request.urlopen(req))


with open("index_template.json", encoding="utf-8") as f:
    print("template", call("PUT", f"{OS}/_index_template/agent-logs", json.load(f)))


def saved(kind, obj_id, attributes, references):
    url = f"{DASH}/api/saved_objects/{kind}/{obj_id}?overwrite=true"
    res = call("POST", url, {"attributes": attributes, "references": references})
    print(kind, res["id"])


def index_ref(pattern_id):
    return [{"name": "kibanaSavedObjectMeta.searchSourceJSON.index", "type": "index-pattern", "id": pattern_id}]


def source(query):
    return json.dumps({
        "indexRefName": "kibanaSavedObjectMeta.searchSourceJSON.index",
        "query": {"language": "kuery", "query": query},
        "filter": [],
    })


for pattern in ("agent-audit", "agent-alerts"):
    saved("index-pattern", pattern, {"title": pattern, "timeFieldName": "@timestamp"}, [])

COLUMNS = ["agent_id", "run_id", "seq", "tool", "args_summary", "approval", "status"]

saved("search", "risky-calls", {
    "title": "위험 도구 호출", "description": "", "hits": 0, "columns": COLUMNS,
    "sort": [["@timestamp", "desc"]], "version": 1,
    "kibanaSavedObjectMeta": {"searchSourceJSON": source("risk:high")},
}, index_ref("agent-audit"))

saved("search", "run-ops-01", {
    "title": "run-ops-01 호출 순서", "description": "", "hits": 0, "columns": COLUMNS,
    "sort": [["@timestamp", "asc"]], "version": 1,
    "kibanaSavedObjectMeta": {"searchSourceJSON": source('run_id:"run-ops-01"')},
}, index_ref("agent-audit"))

saved("search", "alerts", {
    "title": "승인 없는 삭제 경고", "description": "", "hits": 0,
    "columns": ["rule", "severity", "agent_id", "run_id", "args_summary"],
    "sort": [["@timestamp", "desc"]], "version": 1,
    "kibanaSavedObjectMeta": {"searchSourceJSON": source("*")},
}, index_ref("agent-alerts"))

axis = {"id": "ValueAxis-1", "name": "LeftAxis-1", "type": "value", "position": "left", "show": True, "style": {},
        "scale": {"type": "linear", "mode": "normal"}, "labels": {"show": True, "rotate": 0, "filter": False, "truncate": 100},
        "title": {"text": "Count"}}
vis_state = {
    "title": "도구별 호출 수", "type": "histogram",
    "aggs": [
        {"id": "1", "enabled": True, "type": "count", "schema": "metric", "params": {}},
        {"id": "2", "enabled": True, "type": "terms", "schema": "segment",
         "params": {"field": "tool", "size": 5, "order": "desc", "orderBy": "1", "otherBucket": False, "missingBucket": False}},
        {"id": "3", "enabled": True, "type": "terms", "schema": "group",
         "params": {"field": "agent_id", "size": 5, "order": "desc", "orderBy": "1", "otherBucket": False, "missingBucket": False}},
    ],
    "params": {
        "type": "histogram", "grid": {"categoryLines": False},
        "categoryAxes": [{"id": "CategoryAxis-1", "type": "category", "position": "bottom", "show": True, "style": {},
                          "scale": {"type": "linear"}, "labels": {"show": True, "truncate": 100}, "title": {}}],
        "valueAxes": [axis],
        "seriesParams": [{"show": True, "type": "histogram", "mode": "stacked", "data": {"label": "Count", "id": "1"},
                          "valueAxis": "ValueAxis-1", "drawLinesBetweenPoints": True, "showCircles": True}],
        "addTooltip": True, "addLegend": True, "legendPosition": "right", "times": [], "addTimeMarker": False,
        "labels": {"show": True}, "thresholdLine": {"show": False, "value": 10, "width": 1, "style": "full", "color": "#E7664C"},
    },
}
saved("visualization", "calls-by-tool", {
    "title": "도구별 호출 수", "visState": json.dumps(vis_state), "uiStateJSON": "{}", "description": "", "version": 1,
    "kibanaSavedObjectMeta": {"searchSourceJSON": json.dumps({
        "indexRefName": "kibanaSavedObjectMeta.searchSourceJSON.index",
        "query": {"language": "kuery", "query": ""}, "filter": []})},
}, index_ref("agent-audit"))
