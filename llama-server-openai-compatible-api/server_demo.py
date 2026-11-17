"""llama-server 를 127.0.0.1 에만 열고 requests 와 openai 라이브러리로 부른 뒤 서버를 내린다.

준비: llama.cpp Vulkan 빌드(llama-server.exe), GGUF 모델, pip install requests openai
주의: 이 파일이 띄운 서버만 끝낸다. 다른 llama-server 는 건드리지 않는다.
실행: python -X utf8 server_demo.py   (모델 올리는 시간 포함 약 1분)
"""
import subprocess
import time

import requests
from openai import OpenAI

SERVER = r"C:\llama.cpp\llama-server.exe"
MODEL = r"C:\models\Qwen2.5-7B-Instruct-Q4_K_M.gguf"
PORT = 8091
BASE = f"http://127.0.0.1:{PORT}"

proc = subprocess.Popen([SERVER, "-m", MODEL, "--host", "127.0.0.1", "--port", str(PORT),
                         "-ngl", "99", "-c", "4096"],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
try:
    print("## 1. 준비될 때까지 /health 확인")
    t0 = time.time()
    while True:
        try:
            h = requests.get(f"{BASE}/health", timeout=2).json()
            if h.get("status") == "ok":
                break
        except requests.RequestException:
            pass
        time.sleep(1)
    print(f"/health -> ok ({time.time() - t0:.0f}초 걸림)")

    print("## 2. 열린 주소 확인(127.0.0.1 에만 열렸는지)")
    out = subprocess.run(["netstat", "-an"], capture_output=True, text=True).stdout
    print("\n".join(l.strip() for l in out.splitlines() if f":{PORT} " in l and "LISTENING" in l))

    print("## 3. /v1/models")
    print([m["id"] for m in requests.get(f"{BASE}/v1/models").json()["data"]])

    print("## 4. requests 로 부르기(3번, 속도는 서버가 알려 준 값)")
    for i in range(3):
        r = requests.post(f"{BASE}/v1/chat/completions", json={
            "model": "any",
            "messages": [{"role": "user", "content": "한국어로 로컬 AI의 장점을 한 문장으로 말해 주세요."}],
            "max_tokens": 80, "temperature": 0})
        d = r.json()
        print(r.status_code, d["choices"][0]["message"]["content"],
              "| 생성", d["usage"]["completion_tokens"], "토큰,", round(d["timings"]["predicted_per_second"], 1), "토큰/초")

    print("## 5. openai 라이브러리로 부르기")
    c = OpenAI(base_url=f"{BASE}/v1", api_key="none")
    r = c.chat.completions.create(model="any", max_tokens=80, temperature=0,
                                  messages=[{"role": "user", "content": "두 문장으로 자기소개 해 주세요."}])
    print(r.choices[0].message.content, "|", r.usage.completion_tokens, "토큰")

    print("## 6. 스트리밍")
    for ch in c.chat.completions.create(model="any", max_tokens=40, stream=True, temperature=0,
                                        messages=[{"role": "user", "content": "1부터 5까지 세어 주세요."}]):
        print(ch.choices[0].delta.content or "", end="", flush=True)
    print()
finally:
    proc.terminate()
    proc.wait(timeout=30)
    time.sleep(1)
    out = subprocess.run(["netstat", "-an"], capture_output=True, text=True).stdout
    # 접속이 끝난 연결(TIME_WAIT)은 한동안 남으므로 LISTENING 만 센다
    left = [l for l in out.splitlines() if f":{PORT} " in l and "LISTENING" in l]
    print("## 7. 서버 종료 후 8091 LISTENING 줄:", len(left))
