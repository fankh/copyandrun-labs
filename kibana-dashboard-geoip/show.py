import json
for line in open("access-dashboard.ndjson", encoding="utf-8"):
    o = json.loads(line)
    print(o.get("type", "exportDetails"), o.get("id", o.get("exportedCount", "")))
