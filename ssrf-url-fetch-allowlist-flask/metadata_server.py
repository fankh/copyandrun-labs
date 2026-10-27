import json
from http.server import BaseHTTPRequestHandler, HTTPServer

ROUTES = {
    "/": "latest/",
    "/latest/meta-data/": "instance-id\niam/",
    "/latest/meta-data/iam/credentials": json.dumps({
        "AccessKeyId": "FAKEKEY-0000-DEMO",
        "SecretAccessKey": "fake-secret-not-a-real-credential",
        "Token": "fake-session-token-0000",
    }, indent=2),
}


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = ROUTES.get(self.path)
        if body is None:
            self.send_response(404)
            self.end_headers()
            return
        data = body.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, fmt, *args):
        print("내부 서비스가 받은 요청:", self.path)


if __name__ == "__main__":
    print("모의 내부 서비스: http://127.0.0.1:8169")
    HTTPServer(("127.0.0.1", 8169), Handler).serve_forever()
