"""Dashboards 에 인덱스 패턴과 저장된 검색(마스킹 전, 마스킹 후, 원본 번호 검색)을 만듭니다."""
import json
import urllib.request

DASH = "http://127.0.0.1:5791"


def saved(kind, obj_id, attributes, references):
    url = f"{DASH}/api/saved_objects/{kind}/{obj_id}?overwrite=true"
    body = json.dumps({"attributes": attributes, "references": references}).encode()
    req = urllib.request.Request(url, body, {"Content-Type": "application/json", "osd-xsrf": "true"}, method="POST")
    print(kind, json.load(urllib.request.urlopen(req))["id"])


def index_ref(pattern_id):
    return [{"name": "kibanaSavedObjectMeta.searchSourceJSON.index", "type": "index-pattern", "id": pattern_id}]


def source(query):
    return json.dumps({
        "indexRefName": "kibanaSavedObjectMeta.searchSourceJSON.index",
        "query": {"language": "kuery", "query": query},
        "filter": [],
    })


for pattern in ("pii-logs-before", "pii-logs-after", "pii-logs-*"):
    saved("index-pattern", pattern, {"title": pattern, "timeFieldName": "@timestamp"}, [])

COLUMNS = ["logger", "message"]


def search(obj_id, title, pattern, query, columns):
    saved("search", obj_id, {
        "title": title, "description": "", "hits": 0, "columns": columns,
        "sort": [["@timestamp", "asc"]], "version": 1,
        "kibanaSavedObjectMeta": {"searchSourceJSON": source(query)},
    }, index_ref(pattern))


NOISE = "not message:(Press or WARNING)"  # 개발 서버 시작 안내 두 줄은 뺍니다
search("before", "마스킹 전 로그", "pii-logs-before", NOISE, COLUMNS)
search("after", "마스킹 후 로그", "pii-logs-after", NOISE, COLUMNS)
search("raw-search", "원본 번호로 검색", "pii-logs-*", "message:(900101 or 4111 or 8503)", ["mode", "message"])
