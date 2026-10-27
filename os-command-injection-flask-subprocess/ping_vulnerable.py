import subprocess

from flask import Flask, render_template_string, request

app = Flask(__name__)

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


@app.route("/", methods=["GET", "POST"])
def index():
    host = request.form.get("host", "").strip()
    output = None
    if request.method == "POST" and host:
        cmd = "ping -c 1 -W 2 " + host
        result = subprocess.run(cmd, shell=True, capture_output=True,
                                text=True, timeout=15)
        output = "$ " + cmd + "\n" + result.stdout + result.stderr
    return render_template_string(PAGE, host=host, output=output, error=None)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
