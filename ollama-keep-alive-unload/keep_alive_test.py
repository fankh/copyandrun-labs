"""Ollama keep_alive: 모델을 메모리에 얼마나 남길지 호출마다 정하고, ollama ps 로 확인한다.

준비: Ollama 실행 중, ollama pull exaone3.5:2.4b, pip install requests
주의: 이 파일은 exaone3.5:2.4b 만 건드린다. 서비스 전체 설정(OLLAMA_KEEP_ALIVE)은 바꾸지 않는다.
실행: python -X utf8 keep_alive_test.py   (약 40초)
"""
import subprocess
import time
import requests

URL = "http://localhost:11434/api/generate"
MODEL = "exaone3.5:2.4b"


def ps():
    out = subprocess.run(["ollama", "ps"], capture_output=True, text=True).stdout.splitlines()
    rows = [" ".join(l.split()) for l in out[1:] if l.startswith("exaone")]
    return rows or ["(메모리에 없음)"]


def go(keep_alive):
    d = requests.post(URL, json={"model": MODEL, "prompt": "안녕", "stream": False,
                                 "keep_alive": keep_alive, "options": {"num_predict": 5}}, timeout=120).json()
    return round(d["load_duration"] / 1e9, 2)   # 모델을 불러오는 데 걸린 초(이미 올라 있으면 0)


subprocess.run(["ollama", "stop", MODEL], capture_output=True)   # 깨끗한 상태에서 시작
print("keep_alive=0    load", go(0), "| 호출 직후:", ps())
time.sleep(1)
print("keep_alive=20s  load", go("20s"), "| 호출 직후:", ps())
print("바로 한 번 더   load", go("20s"))
time.sleep(25)
print("25초 쉰 뒤:", ps())
print("다시 호출       load", go("0"))
