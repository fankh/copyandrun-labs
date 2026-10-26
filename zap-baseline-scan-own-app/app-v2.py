from flask import Flask, make_response, request
from markupsafe import escape

app = Flask(__name__)


@app.get("/")
def index():
    resp = make_response(
        "<html><head><title>메모 앱</title></head><body>"
        "<h1>메모 앱</h1><p><a href='/login'>로그인</a> | <a href='/memo?q=hello'>메모 검색</a></p>"
        "</body></html>"
    )
    resp.set_cookie("session", "demo-session-value", httponly=True, samesite="Lax")
    return resp


@app.get("/login")
def login():
    return "<html><head><title>로그인</title></head><body><h1>로그인</h1><a href='/'>처음으로</a></body></html>"


@app.get("/memo")
def memo():
    q = request.args.get("q", "")
    return f"<html><head><title>메모</title></head><body><h1>검색어</h1><p>{escape(q)}</p><a href='/'>처음으로</a></body></html>"


@app.after_request
def add_security_headers(resp):
    resp.headers["X-Content-Type-Options"] = "nosniff"
    resp.headers["X-Frame-Options"] = "DENY"
    resp.headers["Content-Security-Policy"] = "default-src 'self'; frame-ancestors 'none'; form-action 'self'"
    resp.headers["Permissions-Policy"] = "geolocation=(), camera=(), microphone=()"
    resp.headers["Cache-Control"] = "no-store"
    resp.headers["Cross-Origin-Opener-Policy"] = "same-origin"
    resp.headers["Cross-Origin-Embedder-Policy"] = "require-corp"
    resp.headers["Cross-Origin-Resource-Policy"] = "same-origin"
    return resp
