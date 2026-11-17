"""설치된 모델의 크기와 한 값당 비트 수를 계산하고, 작은 모델과 큰 모델의 속도를 재고, 메모리에 올라간 상태를 읽는다.

준비: Ollama 실행 중, ollama pull exaone3.5:2.4b, ollama pull gemma4:31b, pip install requests
주의: 모델을 새로 받지 않는다. 큰 모델(20GB)을 메모리에 올리므로 첫 호출에 수십 초가 걸린다.
실행: python -X utf8 size_guide.py   (약 1분)
"""
import re

import requests

URL = "http://localhost:11434"
SMALL, BIG = "exaone3.5:2.4b", "gemma4:31b"

print("## 1. 설치된 모델: 파일 크기와 값 하나당 비트 수")
print(f"{'모델':<30}{'크기':>8}{'매개변수':>9}{'비트/값':>9}  양자화")
for m in requests.get(f"{URL}/api/tags").json()["models"]:
    d = m["details"]
    gb = m["size"] / 1e9
    b = float(re.sub(r"[^0-9.]", "", d["parameter_size"]) or 0) * (1e6 if d["parameter_size"].endswith("M") else 1e9)
    bits = f"{m['size'] * 8 / b:.2f}" if b else "-"
    print(f"{m['name']:<30}{gb:>6.1f}GB{d['parameter_size']:>9}{bits:>9}  {d['quantization_level']}")


def run(model, prompt, **opt):
    d = requests.post(f"{URL}/api/generate", json={"model": model, "prompt": prompt, "stream": False, "think": False,
                                                    "options": {"num_predict": 120, **opt}}, timeout=900).json()
    return d["load_duration"] / 1e9, d["eval_count"] / (d["eval_duration"] / 1e9)


print("\n## 2. 속도(처음 호출의 모델 불러오기와, 이어서 두 번 더 잰 생성 속도)")
print(f"{'모델':<20}{'불러오기':>10}{'생성 속도(토큰/초)':>24}")
for m in (SMALL, BIG):
    load, r1 = run(m, "한국어로 두 문장으로 자기소개 해 주세요.")
    r2 = run(m, "로컬 AI의 장점을 두 문장으로 말해 주세요.")[1]
    r3 = run(m, "방화벽을 한 문장으로 설명해 주세요.")[1]
    print(f"{m:<20}{load:>9.1f}초{r1:>10.1f}{r2:>7.1f}{r3:>7.1f}")

print("\n## 3. 지금 메모리에 올라 있는 모델(ollama ps 와 같은 정보)")
print(f"{'모델':<28}{'올라간 전체':>12}{'그래픽 메모리':>14}{'컨텍스트':>10}")
for m in requests.get(f"{URL}/api/ps").json()["models"]:
    print(f"{m['name']:<28}{m['size'] / 1e9:>10.1f}GB{m['size_vram'] / 1e9:>12.1f}GB{m.get('context_length', '-'):>10}")
