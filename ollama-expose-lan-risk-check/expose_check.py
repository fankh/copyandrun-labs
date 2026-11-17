"""Ollama 를 네트워크에 열면 무엇이 보이는지 임시 인스턴스로 확인한다. 본 서비스(11434)는 건드리지 않는다.

준비: Ollama 설치(ollama 명령), Python 3.9 이상, pip install requests
주의: 11500 포트에 임시 서버를 띄우고 끝에서 이 프로세스만 종료한다. 이 PC 안에서 이 PC의 사설 주소로 접속하는 시험이며 다른 기기 접속은 아니다.
실행: python -X utf8 expose_check.py   (약 30초)
"""
import os
import socket
import subprocess
import time

import requests

MAIN, TEMP = 11434, 11500
MODEL = "exaone3.5:2.4b"


def listeners(port):
    """netstat 에서 해당 포트의 LISTENING 줄을 (주소, PID) 로 돌려준다."""
    out = subprocess.run(["netstat", "-ano"], capture_output=True, text=True).stdout
    rows = []
    for line in out.splitlines():
        p = line.split()
        if len(p) >= 5 and p[0] == "TCP" and p[3] == "LISTENING" and p[1].endswith(f":{port}"):
            rows.append((p[1], p[4]))
    return rows


def lan_ip():
    """이 PC 가 밖으로 나갈 때 쓰는 사설 주소(패킷은 보내지 않는다)."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("10.255.255.255", 1))
    ip = s.getsockname()[0]
    s.close()
    return ip


print("## 1. 본 서비스 11434 가 열린 주소")
for addr, pid in listeners(MAIN):
    print(" ", addr, "PID", pid)

ip = lan_ip()
print(f"\n## 2. 임시 인스턴스를 0.0.0.0:{TEMP} 로 열기 (이 PC 사설 주소 {ip[:ip.rfind('.')]}.x)")
env = dict(os.environ, OLLAMA_HOST=f"0.0.0.0:{TEMP}", OLLAMA_KEEP_ALIVE="0")
proc = subprocess.Popen(["ollama", "serve"], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
try:
    for _ in range(30):
        if listeners(TEMP):
            break
        time.sleep(1)
    for addr, pid in listeners(TEMP):
        print(" ", addr, "PID", pid)

    print(f"\n## 3. 사설 주소로 접속: 로그인 없이 무엇이 되는가")
    base = f"http://{ip}:{TEMP}"
    tags = requests.get(f"{base}/api/tags", timeout=10).json()["models"]
    print(f"  /api/tags  -> 모델 {len(tags)}개 목록이 그대로 보임")
    ver = requests.get(f"{base}/api/version", timeout=10).json()["version"]
    print(f"  /api/version -> {ver}")
    r = requests.post(f"{base}/api/chat", json={"model": MODEL, "stream": False,
                      "options": {"num_predict": 10}, "messages": [{"role": "user", "content": "안녕"}]}, timeout=120)
    print(f"  /api/chat  -> HTTP {r.status_code}, 답: {r.json()['message']['content'][:30]!r}")
    r = requests.get(f"{base}/api/tags", headers={"Authorization": "Bearer wrong-key"}, timeout=10)
    print(f"  틀린 키를 붙여도 -> HTTP {r.status_code} (키를 검사하지 않음)")
finally:
    proc.terminate()
    proc.wait(timeout=30)
    time.sleep(1)

print(f"\n## 4. 종료 후 {TEMP} 포트가 열린 줄 수:", len(listeners(TEMP)))
print("   본 서비스 11434 는 여전히:", [a for a, _ in listeners(MAIN)])
