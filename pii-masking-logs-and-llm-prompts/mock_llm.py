"""모의 LLM 서버입니다. 모델 없이 받은 프롬프트만 기록하고 화면으로 보여 줍니다."""
import html

from flask import Flask, jsonify, request

app = Flask(__name__)
RECEIVED = {"before": [], "after": []}

PAGE = """<!doctype html><meta charset="utf-8"><title>모의 LLM 수신 프롬프트</title>
<style>
body{{font-family:"Malgun Gothic",sans-serif;margin:0;background:#f4f5f7;color:#1c2330}}
header{{background:#1c2330;color:#fff;padding:14px 24px;font-size:18px}}
main{{padding:20px 24px}}
.tag{{display:inline-block;padding:2px 10px;border-radius:10px;color:#fff;background:{color};font-size:14px}}
.card{{background:#fff;border:1px solid #d6dae1;border-radius:6px;padding:12px 16px;margin:12px 0}}
.card h3{{margin:0 0 6px;font-size:14px;color:#566074}}
pre{{margin:0;white-space:pre-wrap;font:15px/1.6 Consolas,"Malgun Gothic",monospace}}
</style>
<header>모의 LLM 서버가 받은 프롬프트</header>
<main><p>수신 구분 <span class="tag">{mode}</span> 총 {count}건</p>{cards}</main>"""


@app.post("/v1/chat")
def chat():
    d = request.get_json()
    RECEIVED[d["mode"]].append(d["prompt"])
    return jsonify(answer="모의 응답: 문의를 접수했습니다.")


@app.post("/reset")
def reset():
    RECEIVED[request.args["mode"]].clear()
    return jsonify(ok=True)


@app.get("/prompts")
def prompts():
    return jsonify(RECEIVED[request.args.get("mode", "before")])


@app.get("/")
def index():
    mode = request.args.get("mode", "before")
    cards = "".join(
        f'<div class="card"><h3>요청 {i}</h3><pre>{html.escape(p)}</pre></div>'
        for i, p in enumerate(RECEIVED[mode], 1)
    )
    color = "#c0392b" if mode == "before" else "#1e8449"
    return PAGE.format(mode="마스킹 전" if mode == "before" else "마스킹 후", color=color, count=len(RECEIVED[mode]), cards=cards)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
