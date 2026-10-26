from flask import Flask, make_response, request

app = Flask(__name__)


@app.get("/")
def index():
    resp = make_response(
        "<html><head><title>메모 앱</title></head><body>"
        "<h1>메모 앱</h1><p><a href='/login'>로그인</a> | <a href='/memo?q=hello'>메모 검색</a></p>"
        "</body></html>"
    )
    resp.set_cookie("session", "demo-session-value")
    return resp


@app.get("/login")
def login():
    return "<html><head><title>로그인</title></head><body><h1>로그인</h1><a href='/'>처음으로</a></body></html>"


@app.get("/memo")
def memo():
    q = request.args.get("q", "")
    return f"<html><head><title>메모</title></head><body><h1>검색어</h1><p>{q}</p><a href='/'>처음으로</a></body></html>"
