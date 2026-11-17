"""Ollama 임베딩(nomic-embed-text)으로 한국어 문장 7개의 코사인 유사도를 재고, 질의로 검색해 본다.

준비: Ollama 실행 중, ollama pull nomic-embed-text, pip install requests numpy
실행: python -X utf8 embed_similarity.py
"""
import numpy as np
import requests

URL = "http://localhost:11434/api/embed"
MODEL = "nomic-embed-text"

S = ["비밀번호를 잊어버렸을 때 재설정하는 방법",     # 0
     "계정 암호 복구 절차 안내",                      # 1  0과 같은 뜻
     "점심 메뉴로 김치찌개를 먹었다",                 # 2
     "오늘 저녁에는 된장찌개가 먹고 싶다",            # 3  2와 같은 주제(음식)
     "서버 디스크 사용량이 90퍼센트를 넘었다",        # 4
     "저장 공간이 부족해서 로그 파일을 지웠다",       # 5  4와 같은 주제(용량)
     "다음 주 월요일 오전 10시에 회의가 있습니다"]    # 6


def embed(texts):
    r = requests.post(URL, json={"model": MODEL, "input": texts}, timeout=120).json()
    v = np.array(r["embeddings"])
    return v / np.linalg.norm(v, axis=1, keepdims=True)  # 길이를 1로 맞추면 내적이 코사인 유사도


print("== 1. 벡터 만들기")
E = embed(S)
print("shape", E.shape)

print("== 2. 문장마다 가장 가까운 문장")
M = E @ E.T
for i, s in enumerate(S):
    j = max((k for k in range(len(S)) if k != i), key=lambda k: M[i, k])
    print(f"{i} -> {j} sim {M[i, j]:.3f} | {s[:16]} / {S[j][:16]}")

print("== 3. 전체 유사도 표(7x7)")
print("    " + " ".join(f"{k:5d}" for k in range(len(S))))
for i in range(len(S)):
    print(f"{i:3d} " + " ".join(f"{M[i, k]:5.2f}" for k in range(len(S))))
tri = M[np.triu_indices(len(S), 1)]
print("서로 다른 문장 쌍 21개의 범위: %.3f ~ %.3f" % (tri.min(), tri.max()))

print("== 4. 질의로 검색: 암호를 까먹었어요")
q = embed(["암호를 까먹었어요"])[0]
sc = E @ q
for k in np.argsort(-sc)[:3]:
    print(f"{sc[k]:.3f} {S[k]}")
