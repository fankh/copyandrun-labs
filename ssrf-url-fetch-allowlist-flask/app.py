import re

import requests
from flask import Flask, render_template_string, request

app = Flask(__name__)

PAGE = """<!doctype html>
<meta charset="utf-8">
<title>링크 미리보기</title>
<style>
  body { font-family: "Malgun Gothic", sans-serif; max-width: 720px; margin: 40px auto; color: #222; }
  input[name=url] { width: 70%; padding: 8px; }
  button { padding: 8px 16px; }
  .card { border: 1px solid #ccc; border-radius: 6px; padding: 16px; margin-top: 20px; }
  .err { border-color: #c0392b; background: #fdecea; }
  pre { background: #f4f4f4; padding: 10px; white-space: pre-wrap; word-break: break-all; }
</style>
<h1>링크 미리보기</h1>
<form method="get" action="/">
  <input name="url" value="{{ url }}" placeholder="https://example.com">
  <button>미리보기</button>
</form>
{% if error %}
<div class="card err"><b>거부 또는 실패</b><p>{{ error }}</p></div>
{% elif result %}
<div class="card">
  <p><b>주소</b> {{ url }}</p>
  <p><b>상태</b> {{ result.status }}</p>
  <p><b>제목</b> {{ result.title }}</p>
  <b>본문 앞부분</b>
  <pre>{{ result.snippet }}</pre>
</div>
{% endif %}
"""


def summarize(text, status):
    m = re.search(r"<title>(.*?)</title>", text, re.I | re.S)
    title = m.group(1).strip() if m else "(제목 없음)"
    return {"status": status, "title": title, "snippet": text[:400]}


@app.route("/")
def index():
    url = request.args.get("url", "").strip()
    result = error = None
    if url:
        try:
            r = requests.get(url, timeout=5)
            result = summarize(r.content.decode("utf-8", "replace"), r.status_code)
        except requests.RequestException as e:
            error = "가져오지 못했습니다: %s" % type(e).__name__
    return render_template_string(PAGE, url=url, result=result, error=error)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5071)
