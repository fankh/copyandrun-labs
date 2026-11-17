#!/usr/bin/env python3
# 사용: python bola_lab.py
# 127.0.0.1 에 시험용 주문 API 를 임시로 띄워, 같은 요청이 취약한 판과 고친 판에서 어떻게 다른지 확인한다.
# BOLA(객체 수준 권한 검증 누락): 로그인은 했지만 남의 주문 번호를 넣어도 조회되는 문제.
# 토큰은 시험용 문자열이고, 서버는 스크립트가 끝나면 함께 종료된다.
import json
import threading
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer

TOKENS = {"token-alice": "alice", "token-bob": "bob"}
ORDERS = {1: {"owner": "alice", "item": "keyboard"}, 2: {"owner": "bob", "item": "monitor"}}


def make_handler(check_owner):
    class H(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def reply(self, code, body):
            data = json.dumps(body).encode()
            self.send_response(code)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(data)

        def do_GET(self):
            user = TOKENS.get(self.headers.get("Authorization", "").replace("Bearer ", ""))
            if not user:
                return self.reply(401, {"error": "login required"})
            order = ORDERS.get(int(self.path.rsplit("/", 1)[1]))
            if not order:
                return self.reply(404, {"error": "not found"})
            if check_owner and order["owner"] != user:
                return self.reply(404, {"error": "not found"})
            return self.reply(200, order)

    return H


def get(port, order_id, token):
    req = urllib.request.Request(f"http://127.0.0.1:{port}/orders/{order_id}", headers={"Authorization": f"Bearer {token}"})
    try:
        with urllib.request.urlopen(req) as r:
            return r.status, r.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()


for label, check_owner, port in (("취약한 판", False, 18091), ("고친 판", True, 18092)):
    server = HTTPServer(("127.0.0.1", port), make_handler(check_owner))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    print(f"== {label}")
    print("alice 가 자기 주문 1 조회:", *get(port, 1, "token-alice"))
    print("alice 가 bob 의 주문 2 조회:", *get(port, 2, "token-alice"))
    server.shutdown()
