import ipaddress
import re
import socket
from urllib.parse import urljoin, urlparse

import requests
from flask import Flask, render_template_string, request

app = Flask(__name__)

MAX_BYTES = 1024 * 1024
MAX_REDIRECTS = 3
TIMEOUT = (3, 5)

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


class Blocked(Exception):
    pass


def check_url(url):
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        raise Blocked("http 와 https 주소만 허용합니다.")
    if not parsed.hostname:
        raise Blocked("주소에 호스트가 없습니다.")
    try:
        port = parsed.port or (443 if parsed.scheme == "https" else 80)
        infos = socket.getaddrinfo(parsed.hostname, port, proto=socket.IPPROTO_TCP)
    except (ValueError, socket.gaierror):
        raise Blocked("주소를 해석하지 못했습니다.")
    for info in infos:
        ip = ipaddress.ip_address(info[4][0].split("%")[0])
        if ip.version == 6 and ip.ipv4_mapped:
            ip = ip.ipv4_mapped
        if not ip.is_global:
            raise Blocked("내부 주소(%s)로 연결되는 주소는 허용하지 않습니다." % ip)


def safe_fetch(url):
    for _ in range(MAX_REDIRECTS + 1):
        check_url(url)
        r = requests.get(url, timeout=TIMEOUT, allow_redirects=False, stream=True)
        if r.status_code in (301, 302, 303, 307, 308) and "Location" in r.headers:
            url = urljoin(url, r.headers["Location"])
            r.close()
            continue
        body = b""
        for chunk in r.iter_content(8192):
            body += chunk
            if len(body) > MAX_BYTES:
                r.close()
                raise Blocked("응답이 1MB를 넘어 중단했습니다.")
        r.close()
        return r.status_code, body
    raise Blocked("리디렉션이 %d번을 넘었습니다." % MAX_REDIRECTS)


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
            status, body = safe_fetch(url)
            result = summarize(body.decode("utf-8", "replace"), status)
        except Blocked as e:
            error = str(e)
        except requests.RequestException as e:
            error = "가져오지 못했습니다: %s" % type(e).__name__
    return render_template_string(PAGE, url=url, result=result, error=error)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5071)
