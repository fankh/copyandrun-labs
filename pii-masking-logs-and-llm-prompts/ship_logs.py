"""앱이 남긴 JSON 로그 파일을 OpenSearch 에 색인합니다. 마스킹 전은 pii-logs-before, 후는 pii-logs-after 입니다."""
import json
import sys
import urllib.error
import urllib.request

OS = "http://127.0.0.1:5790"


def call(method, path, body=None, ctype="application/json"):
    data = body.encode() if isinstance(body, str) else None
    req = urllib.request.Request(OS + path, data, {"Content-Type": ctype}, method=method)
    with urllib.request.urlopen(req) as res:
        return json.load(res)


for mode in sys.argv[1:] or ("before", "after"):  # 인자로 before 또는 after 하나만 줄 수도 있습니다
    index = f"pii-logs-{mode}"
    try:
        call("DELETE", f"/{index}")
    except urllib.error.HTTPError:
        pass  # 처음 실행이면 지울 색인이 없습니다
    with open(f"logs/app-{mode}.log", encoding="utf-8") as f:
        docs = [line for line in f.read().splitlines() if line.strip()]
    bulk = "".join(f'{{"index":{{"_index":"{index}"}}}}\n{d}\n' for d in docs)
    res = call("POST", "/_bulk?refresh=true", bulk, "application/x-ndjson")
    print(index, len(docs), "건", "오류 있음" if res["errors"] else "오류 없음")
