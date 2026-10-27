import secrets
from flask import Flask, request, redirect, make_response, render_template_string, g

app = Flask(__name__)
POSTS = [{"title": "공지", "body": "실습용 게시판입니다."}]

PAGE = """<!doctype html><meta charset="utf-8"><title>게시판</title><link rel="icon" href="data:,">
<h1>게시판</h1>
<p id="banner"></p>
<form method="post" action="/post">
  <input name="title" placeholder="제목"><br>
  <textarea name="body" placeholder="내용"></textarea><br>
  <button>등록</button>
</form>
<p>최근 글: <span id="latest"></span></p>
{% for p in posts %}<article><h3>{{ p.title }}</h3><div>{{ p.body }}</div></article>{% endfor %}
<script nonce="{{ nonce }}">document.getElementById("latest").textContent = {{ latest|tojson }};</script>"""


@app.before_request
def make_nonce():
    g.nonce = secrets.token_urlsafe(16)


@app.after_request
def security_headers(resp):
    resp.headers["Content-Security-Policy"] = (
        "default-src 'self'; script-src 'nonce-%s'; img-src 'self' data:; object-src 'none'; "
        "base-uri 'none'; frame-ancestors 'none'" % g.nonce)
    return resp


@app.route("/")
def index():
    resp = make_response(render_template_string(
        PAGE, posts=POSTS, latest=POSTS[-1]["title"], nonce=g.nonce))
    resp.set_cookie("sid", "demo-session-1234", httponly=True, samesite="Lax")
    return resp


@app.route("/post", methods=["POST"])
def post():
    POSTS.append({"title": request.form.get("title", ""),
                  "body": request.form.get("body", "")})
    return redirect("/")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5100)
