"""PyPI JSON API 와 같은 모양으로 응답하는 연습용 가짜 인덱스입니다. 실제 PyPI 와 무관합니다."""
import json
from datetime import datetime, timedelta, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer


def pkg(releases):
    """releases: [(버전, 며칠 전 업로드)]"""
    now = datetime.now(timezone.utc)
    return {"info": {}, "releases": {
        v: [{"upload_time_iso_8601": (now - timedelta(days=d)).strftime("%Y-%m-%dT%H:%M:%S.000000Z")}]
        for v, d in releases}}


DB = {
    "requests": pkg([(f"2.{i}.0", 4000 - i * 100) for i in range(30)]),
    "flask": pkg([(f"3.{i}.0", 900 - i * 50) for i in range(10)]),
    "fresh-yaml-tools": pkg([("0.1.0", 2)]),
    "reqeusts": pkg([("0.0.1", 1)]),
}


class H(BaseHTTPRequestHandler):
    def do_GET(self):
        parts = self.path.strip("/").split("/")
        data = DB.get(parts[1]) if len(parts) == 3 and parts[0] == "pypi" and parts[2] == "json" else None
        body = json.dumps(data if data else {"message": "Not Found"}).encode()
        self.send_response(200 if data else 404)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


HTTPServer(("0.0.0.0", 8000), H).serve_forever()
