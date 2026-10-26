import json
import urllib.request

docs = []
for i in range(120):
    docs.append({"@timestamp": "2026-10-15T09:%02d:%02dZ" % (i // 60, i % 60), "source.ip": "10.13.37.7",
                 "url.path": "/login", "http.response.status_code": 401, "user_agent.original": "python-requests/2.31"})
for i in range(40):
    docs.append({"@timestamp": "2026-10-15T09:%02d:00Z" % i, "source.ip": "192.168.10.%d" % (i + 2),
                 "url.path": "/index.html", "http.response.status_code": 200, "user_agent.original": "Mozilla/5.0"})
docs.append({"@timestamp": "2026-10-15T09:30:00Z", "source.ip": "192.168.10.99", "url.path": "/api/items",
             "url.query": "id=1 UNION SELECT username,password FROM users",
             "http.response.status_code": 200, "user_agent.original": "sqlmap/1.7"})
body = "".join(json.dumps({"index": {"_index": "security-web"}}) + "\n" + json.dumps(d) + "\n" for d in docs)
req = urllib.request.Request("http://opensearch:9200/_bulk?refresh=true", body.encode(), {"Content-Type": "application/x-ndjson"})
print(json.load(urllib.request.urlopen(req))["errors"])
