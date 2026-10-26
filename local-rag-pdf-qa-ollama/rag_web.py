from html import escape
from string import Template

from flask import Flask, request

import rag

app = Flask(__name__)
PDF = "company_rules.pdf"
INDEX = {}

PAGE = Template("""<!doctype html>
<html lang="ko"><meta charset="utf-8">
<title>PDF 질문 답변 화면</title>
<style>
body{font-family:"Malgun Gothic",sans-serif;margin:0;background:#f4f5f7;color:#1f2933}
header{background:#1f2933;color:#fff;padding:14px 28px;font-size:18px}
main{padding:20px 28px;max-width:1000px}
form{background:#fff;border:1px solid #d5d9de;border-radius:8px;padding:14px 18px;display:flex;gap:12px;flex-wrap:wrap}
input[name=q]{flex:1;min-width:360px;font:inherit;padding:7px 9px;border:1px solid #aab2bb;border-radius:4px}
button{font:inherit;padding:7px 18px;background:#2a6fdb;color:#fff;border:0;border-radius:4px}
.answer{font-size:19px;background:#e8f0fe;border:1px solid #2a6fdb;border-radius:8px;padding:14px 18px;margin-top:14px}
.box{background:#fff;border:1px solid #d5d9de;border-radius:8px;padding:12px 16px;margin-top:14px}
.box h2{margin:0 0 8px;font-size:16px}
.ev{padding:8px 10px;border-radius:6px;margin:6px 0;background:#eef2f6;font-size:14px}
.ev b{display:inline-block;min-width:150px}
.hint{font-size:13px;color:#52606d;margin-top:8px}
</style>
<header>사내 규정 PDF에 묻고 답하기 (Ollama 로컬 RAG)</header>
<main>
<form method="get">
<input name="q" value="${q}" placeholder="질문을 입력하세요">
<button>질문하기</button>
</form>
${result}
</main></html>""")


def get_index():
    if not INDEX:
        INDEX["chunks"] = rag.build_index(PDF)
    return INDEX["chunks"]


@app.get("/")
def index():
    q = request.args.get("q", "")
    result = ""
    if q:
        idx = get_index()
        qv = rag.embed(["search_query: " + q])[0]
        answer, hits = rag.ask(idx, q)
        rows = ""
        for i, h in enumerate(hits, 1):
            score = rag.cosine(qv, h["vec"])
            rows += (f'<div class="ev"><b>[{i}] p.{h["page"]} 유사도 {score:.3f}</b>'
                     f'{escape(h["text"].replace(chr(10), " "))}</div>')
        result = (f'<div class="answer">{escape(answer)}</div>'
                  f'<div class="box"><h2>근거로 넣은 조각 (위에서부터 [1], [2], [3])</h2>{rows}'
                  '<div class="hint">모델이 답 끝에 붙이는 번호에 기대지 말고, 이 목록과 답의 숫자를 직접 대조합니다.</div></div>')
    return PAGE.substitute(q=escape(q, quote=True), result=result)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5404)
