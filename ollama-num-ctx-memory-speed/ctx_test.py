"""Ollama num_ctx 실험 두 가지.
  1. 짧은 질문으로 num_ctx 를 2048, 8192, 32768 로 바꿔 메모리, 불러오는 시간, 생성 속도를 잰다.
  2. 긴 글 맨 앞에 비밀 코드를 적고, 글을 끝까지 넣은 뒤 코드를 묻는다(num_ctx 에 따라 앞부분을 잊는지 본다).

준비: Ollama 실행 중, 모델 exaone3.5:2.4b 와 qwen2.5:3b-instruct-q4_K_M (ollama pull 로 받는다), pip install requests
실행: python -X utf8 ctx_test.py
"""
import subprocess
import time
import requests

URL = "http://localhost:11434/api/generate"
MODEL = "exaone3.5:2.4b"
MODEL2 = "qwen2.5:3b-instruct-q4_K_M"   # 2번 실험용(앞부분 기억 시험)


def ps_row():
    out = subprocess.run(["ollama", "ps"], capture_output=True, text=True).stdout.splitlines()
    rows = [l for l in out if l.startswith(MODEL.split(":")[0])]
    return " ".join(rows[0].split()) if rows else "(내려감)"


def ask(prompt, num_ctx, num_predict=60, model=MODEL):
    t = time.time()
    d = requests.post(URL, json={"model": model, "prompt": prompt, "stream": False,
                                 "options": {"num_ctx": num_ctx, "num_predict": num_predict, "temperature": 0}},
                      timeout=600).json()
    d["wall"] = time.time() - t
    return d


print("== 1. 짧은 질문: num_ctx 별 메모리와 속도")
for n in (2048, 8192, 32768):
    d = ask("한국어로 한 문장만 인사해 주세요.", n)
    print(n, "load %.1fs" % (d["load_duration"] / 1e9),
          "eval %.1f tok/s" % (d["eval_count"] / (d["eval_duration"] / 1e9)), "|", ps_row())

print("== 2. 긴 글 맨 앞의 코드를 기억하나 (모델 %s)" % MODEL2)
CODE = "ZEBRA-4417"
KINDS = ["웹", "DB", "캐시", "배치"]


def make_prompt(items):
    filler = "".join("%d번 서버(%s)의 디스크 사용률은 %d퍼센트이고 점검자는 %s입니다. "
                     % (i, KINDS[i % 4], 40 + (i * 7) % 50, "김이박최정"[i % 5]) for i in range(1, items + 1))
    return ("[중요] 이 문서의 비밀 코드는 %s 입니다.\n" % CODE + filler +
            "\n질문: 이 문서 맨 앞에 적힌 비밀 코드는 무엇입니까? 코드만 답하세요.")


for items in (30, 160):
    prompt = make_prompt(items)
    for n in (2048, 8192):
        d = ask(prompt, n, num_predict=30, model=MODEL2)
        ans = d["response"].strip().replace("\n", " ")
        print("서버 %3d줄 | num_ctx %-5d 읽은 입력 %5d토큰 | 입력 처리 %.0f tok/s | 총 %.1fs | 답: %-12s %s"
              % (items, n, d["prompt_eval_count"], d["prompt_eval_count"] / (d["prompt_eval_duration"] / 1e9),
                 d["wall"], ans[:12], "정답" if CODE in ans else "오답"))
