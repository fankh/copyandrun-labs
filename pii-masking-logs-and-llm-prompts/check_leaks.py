"""마스킹 전후 로그와 LLM 수신 프롬프트에 개인정보 모양이 남았는지 느슨한 규칙으로 셉니다."""
import json
import re
import urllib.request

LLM = "http://127.0.0.1:5793"
LOOSE = {
    "주민번호": re.compile(r"\d{6}-?[1-4]\d{6}"),
    "휴대전화": re.compile(r"01[016789][-. ]?\d{3,4}[-. ]?\d{4}"),
    "이메일": re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+"),
    "카드번호": re.compile(r"\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}"),
}


def count(texts):
    return {name: sum(1 for t in texts if pat.search(t)) for name, pat in LOOSE.items()}


def show(label, hits):
    print(f"{label:<14}" + "  ".join(f"{k} {v}" for k, v in hits.items()))


for mode in ("before", "after"):
    logs = []
    with open(f"logs/app-{mode}.log", encoding="utf-8") as f:
        for row in f:
            if row.strip():
                doc = json.loads(row)
                logs.append(doc["message"] + doc.get("exception", ""))
    with urllib.request.urlopen(f"{LLM}/prompts?mode={mode}") as res:
        prompts = json.load(res)
    show(f"로그 {mode}", count(logs))
    show(f"프롬프트 {mode}", count(prompts))
