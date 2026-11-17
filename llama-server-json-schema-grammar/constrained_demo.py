"""llama-server 의 출력 제한(JSON 스키마, GBNF 문법)으로 작은 모델의 출력 형식을 고정하고, 제한이 없을 때와 비교한다.

준비: llama.cpp Vulkan 빌드(llama-server.exe), GGUF 모델 두 개, pip install requests
주의: 이 파일이 띄운 서버(127.0.0.1:8093)만 끝낸다. 다른 llama-server 는 건드리지 않는다.
실행: python -X utf8 constrained_demo.py   (약 2분)
"""
import json
import subprocess
import time

import requests

SERVER = r"C:\llama.cpp\llama-server.exe"
MODELS = {"Llama 3.2 1B": r"C:\models\Llama-3.2-1B-Instruct-Q4_K_M.gguf",
          "Qwen2.5 7B": r"C:\models\Qwen2.5-7B-Instruct-Q4_K_M.gguf"}
PORT = 8093
BASE = f"http://127.0.0.1:{PORT}"
CATS = ["결제", "로그인", "배송", "기타"]
PRIS = ["높음", "보통", "낮음"]

# (문의 내용, 정답 분류, 정답 우선순위). 실습용으로 직접 만든 문장과 라벨이다.
TICKETS = [
    ("카드 결제가 두 번 됐어요. 빨리 환불해 주세요.", "결제", "높음"),
    ("비밀번호를 바꾸고 싶은데 메뉴를 못 찾겠어요.", "로그인", "낮음"),
    ("주문한 지 일주일인데 배송이 아직 시작도 안 했습니다.", "배송", "보통"),
    ("로그인이 계속 실패합니다. 내일 아침까지 써야 해요.", "로그인", "높음"),
    ("영수증을 이메일로 다시 받을 수 있나요?", "결제", "낮음"),
    ("택배가 다른 주소로 갔다고 합니다. 어떻게 하죠?", "배송", "높음"),
    ("앱 디자인이 예뻐졌네요. 의견 드립니다.", "기타", "낮음"),
    ("인증 문자가 오지 않아서 가입을 못 하고 있어요.", "로그인", "보통"),
    ("결제 수단을 바꾸고 싶습니다.", "결제", "낮음"),
    ("포장이 심하게 훼손된 채로 왔어요. 교환 부탁드립니다.", "배송", "보통"),
    ("회사 연락처가 어디 있나요?", "기타", "낮음"),
    ("계정이 도용된 것 같아요. 모르는 결제 알림이 왔습니다.", "로그인", "높음"),
]
SYSTEM = ("고객 문의를 분류한다. 분류는 결제, 로그인, 배송, 기타 중 하나이고 "
          "우선순위는 높음, 보통, 낮음 중 하나다. 한 줄 요약도 쓴다. 다른 말은 하지 않는다.")
SCHEMA = {"type": "object",
          "properties": {"category": {"enum": CATS}, "priority": {"enum": PRIS}, "summary": {"type": "string"}},
          "required": ["category", "priority", "summary"], "additionalProperties": False}
# 라벨 한 단어만 허용하는 GBNF 문법(root 가 이 중 하나로만 시작하고 끝난다)
GRAMMAR = 'root ::= "결제" | "로그인" | "배송" | "기타"'


def start(path):
    p = subprocess.Popen([SERVER, "-m", path, "--host", "127.0.0.1", "--port", str(PORT), "-ngl", "99", "-c", "4096"],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(90):
        try:
            if requests.get(BASE + "/health", timeout=2).json().get("status") == "ok":
                return p
        except (requests.RequestException, ValueError):
            pass
        time.sleep(1)
    p.kill()
    raise RuntimeError("서버가 시작되지 않았다")


def ask(user, **extra):
    body = {"model": "any", "temperature": 0, "max_tokens": 120,
            "messages": [{"role": "system", "content": SYSTEM}, {"role": "user", "content": user}]}
    body.update(extra)
    t = time.time()
    d = requests.post(BASE + "/v1/chat/completions", json=body, timeout=120).json()
    return d["choices"][0]["message"]["content"], d["usage"]["completion_tokens"], time.time() - t


def judge(text):
    """JSON 으로 읽히는가 / 키와 값이 스키마에 맞는가 -> (읽힘, 맞음, 분류, 우선순위)"""
    try:
        j = json.loads(text)
    except ValueError:
        return False, False, None, None
    ok = (isinstance(j, dict) and j.get("category") in CATS and j.get("priority") in PRIS
          and isinstance(j.get("summary"), str))
    return True, ok, j.get("category") if isinstance(j, dict) else None, j.get("priority") if isinstance(j, dict) else None


MODES = {
    "제한 없음(프롬프트로만 JSON 요청)": lambda u: ask(u + '\n\nJSON 한 개로만 답하라. 키: category, priority, summary.'),
    "json_schema 로 제한": lambda u: ask(u, response_format={"type": "json_schema", "json_schema": {"name": "t", "schema": SCHEMA}}),
}

results = {}
for name, path in MODELS.items():
    srv = start(path)
    try:
        print(f"\n[{name}] 서버 준비됨")
        for mode, fn in MODES.items():
            parsed = valid = cat_ok = pri_ok = toks = 0
            secs = 0.0
            first = None
            for text, cat, pri in [(t[0], t[1], t[2]) for t in TICKETS]:
                out, n, dt = fn(text)
                p, v, c, pr = judge(out)
                parsed += p
                valid += v
                cat_ok += (c == cat)
                pri_ok += (pr == pri)
                toks += n
                secs += dt
                if first is None:
                    first = out.replace("\n", " ")[:60]
            N = len(TICKETS)
            results[(name, mode)] = (parsed, valid, cat_ok, pri_ok, toks / secs)
            print(f"  {mode}\n    JSON 으로 읽힘 {parsed}/{N}, 스키마에 맞음 {valid}/{N}, 분류 정답 {cat_ok}/{N}, 우선순위 정답 {pri_ok}/{N}, {toks / secs:.0f}토큰/초(요청 전체 시간 기준)")
            print(f"    첫 출력: {first}")
        # GBNF 문법: 분류 라벨 한 단어만 허용
        ok = same = 0
        outs = []
        for text, cat, pri in TICKETS:
            out, n, dt = ask(text + "\n분류 하나만 답하라.", grammar=GRAMMAR)
            outs.append(out)
            ok += out in CATS
            same += (out == cat)
        print(f"  GBNF 문법(라벨 한 단어만 허용)\n    허용된 단어만 나옴 {ok}/{len(TICKETS)}, 분류 정답 {same}/{len(TICKETS)}, 출력 예 {outs[:4]}")
    finally:
        srv.terminate()
        srv.wait(timeout=30)
        time.sleep(1)

print("\n## 요약: 스키마에 맞는 출력 수(12건 중)")
for (m, mode), r in results.items():
    print(f"  {m:<14} {'제한 없음' if mode.startswith('제한') else 'json_schema':<12} 스키마 {r[1]:>2}/12  분류 정답 {r[2]:>2}/12  우선순위 정답 {r[3]:>2}/12")
