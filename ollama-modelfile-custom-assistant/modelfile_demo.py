"""Ollama Modelfile 로 사내 IT 도우미 모델을 만들고, 원본과 같은 질문 세 개로 답을 비교한 뒤 지운다.

준비: Ollama 실행 중, ollama pull exaone3.5:2.4b, pip install requests
주의: 만든 모델 이름은 it-helper-demo 이고 끝에서 이 모델만 지운다. 원본 모델은 건드리지 않는다.
실행: python -X utf8 modelfile_demo.py   (약 40초)
"""
import subprocess
from pathlib import Path

import requests

BASE = "exaone3.5:2.4b"
NEW = "it-helper-demo"
URL = "http://localhost:11434/api/chat"
QS = ["회사 노트북 비밀번호를 잊어버렸습니다. 어떻게 해야 하나요?",
      "VPN이 자꾸 끊깁니다. 무엇부터 확인하면 되나요?",
      "프린터에서 출력이 안 됩니다. 어떻게 하죠?"]

MODELFILE = f'''FROM {BASE}
SYSTEM """당신은 사내 IT 도우미입니다. 항상 존댓말로, 세 문장 이내로 답합니다."""
PARAMETER temperature 0.2
PARAMETER num_ctx 4096
'''
Path("Modelfile").write_text(MODELFILE, encoding="utf-8")

print("## 1. ollama create")
r = subprocess.run(["ollama", "create", NEW, "-f", "Modelfile"], capture_output=True, text=True, encoding="utf-8")
print("success" if "success" in (r.stdout + r.stderr) else "실패: " + r.stderr)   # 진행 표시 제어문자는 출력하지 않는다

print("## 2. ollama show --modelfile (줄 앞부분만)")
out = subprocess.run(["ollama", "show", NEW, "--modelfile"], capture_output=True, text=True, encoding="utf-8").stdout
for line in out.splitlines():
    if line.startswith(("FROM", "SYSTEM", "PARAMETER")):
        print(line[:70])


def ask(model, q):
    d = requests.post(URL, json={"model": model, "stream": False, "options": {"seed": 1},
                                 "messages": [{"role": "user", "content": q}]}, timeout=300).json()
    text = d["message"]["content"].strip()
    return d["eval_count"], len(text), text


print("## 3. 같은 질문 세 개, 원본과 비교(토큰 수 / 글자 수)")
print(f"{'질문':<4} {BASE:>16} {NEW:>18}")
last = {}
for i, q in enumerate(QS, 1):
    a = ask(BASE, q)
    b = ask(NEW, q)
    last[i] = b[2]
    print(f"{i:<4} {a[0]:>6}토큰/{a[1]:>4}자 {b[0]:>8}토큰/{b[1]:>4}자")

print("## 4. it-helper-demo 의 답(질문 1)")
print(last[1])

print("## 5. 정리")
print(subprocess.run(["ollama", "rm", NEW], capture_output=True, text=True, encoding="utf-8").stdout.strip())
names = subprocess.run(["ollama", "list"], capture_output=True, text=True, encoding="utf-8").stdout
print("원본 남음:", BASE in names, "| 만든 모델 남음:", NEW in names)
Path("Modelfile").unlink()
