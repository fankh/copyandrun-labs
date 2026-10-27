import ipaddress
import subprocess

from flask import Flask, render_template_string, request

app = Flask(__name__)

ALLOWED_NETWORKS = [
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
]

PAGE = """<!doctype html>
<meta charset="utf-8">
<title>호스트 점검 도구</title>
<style>
  body { font-family: sans-serif; max-width: 640px; margin: 40px auto; }
  input[name=host] { width: 320px; padding: 6px; }
  button { padding: 6px 14px; }
  pre { background: #111; color: #eee; padding: 12px; white-space: pre-wrap; }
  .msg { padding: 8px 12px; background: #fde8e8; border: 1px solid #e0a0a0; }
</style>
<h1>호스트 점검 도구</h1>
<form method="post">
  <input name="host" value="{{ host }}" placeholder="점검할 호스트 주소">
  <button>ping 점검</button>
</form>
{% if error %}<p class="msg">{{ error }}</p>{% endif %}
{% if output %}<h3>실행 결과</h3><pre>{{ output }}</pre>{% endif %}
"""


def parse_target(text):
    try:
        addr = ipaddress.ip_address(text)
    except ValueError:
        return None, "IP 주소 형식이 아닙니다."
    if not any(addr in net for net in ALLOWED_NETWORKS):
        return None, "점검 허용 대역(내부망)이 아닙니다."
    return str(addr), None


@app.route("/", methods=["GET", "POST"])
def index():
    host = request.form.get("host", "").strip()
    output = None
    error = None
    if request.method == "POST" and host:
        target, error = parse_target(host)
        if target:
            args = ["ping", "-c", "1", "-W", "2", target]
            result = subprocess.run(args, capture_output=True,
                                    text=True, timeout=15)
            output = "$ " + " ".join(args) + "\n" + result.stdout + result.stderr
    return render_template_string(PAGE, host=host, output=output, error=error)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
