"""Ollama 임베딩 심화: 한국어 문서 열두 개에서 질문으로 문서를 찾는 시험. 모델 두 개 비교, 접두어(search_query:/search_document:) 유무, 임계값.

준비: Ollama 실행 중, ollama pull nomic-embed-text bge-m3, pip install requests numpy
실행: python -X utf8 emb_more.py   (약 20초)
"""
import numpy as np
import requests

URL = "http://localhost:11434/api/embed"
MODELS = ["nomic-embed-text", "bge-m3"]

DOCS = [
    "비밀번호를 잊어버렸을 때는 로그인 화면의 재설정 링크로 이메일 인증을 거쳐 새 비밀번호를 정합니다.",
    "연차 휴가는 입사 1년 뒤부터 15일이 주어지며 사용 전에 팀장에게 신청해야 합니다.",
    "VPN에 접속하려면 사내 인증서를 설치한 뒤 지정된 주소로 접속하고 일회용 코드를 입력합니다.",
    "노트북을 분실하면 즉시 보안팀에 알리고 원격 삭제를 요청해야 합니다.",
    "회의실 예약은 사내 포털의 달력에서 시간과 인원을 선택해 신청합니다.",
    "출장비는 귀국 후 7일 안에 영수증을 첨부해 정산 시스템에 제출합니다.",
    "서버 디스크 사용률이 90퍼센트를 넘으면 운영팀에 알림이 가고 오래된 로그를 정리합니다.",
    "개인정보가 들어 있는 파일은 암호화한 뒤 승인된 저장소에만 보관해야 합니다.",
    "신입 사원 교육은 입사 첫 주에 보안 수칙과 업무 도구 사용법을 다룹니다.",
    "프린터 용지가 떨어지면 총무팀 보관함에서 가져다 넣고 사용 기록에 적습니다.",
    "소프트웨어 설치가 필요하면 IT 지원 포털에 요청서를 내고 승인을 받아야 합니다.",
    "퇴사자의 계정은 마지막 근무일에 비활성화하고 30일 뒤 삭제합니다.",
]
# (질문, 정답 문서 번호). 질문은 문서의 낱말을 일부러 피해 다르게 적었다.
QUERIES = [
    ("암호가 기억나지 않아요", 0), ("쉬는 날은 며칠이나 쓸 수 있나요", 1), ("집에서 회사 네트워크에 들어가려면", 2),
    ("컴퓨터를 잃어버렸어요", 3), ("회의할 장소를 잡고 싶어요", 4), ("출장 갔다 온 비용 돌려받기", 5),
    ("저장 공간이 거의 찼을 때 어떻게 되나요", 6), ("고객 정보 파일을 어디에 두나요", 7),
    ("새로 들어온 사람은 무엇을 배우나요", 8), ("복사 용지 채우는 방법", 9),
    ("프로그램을 깔고 싶은데요", 10), ("그만둔 직원의 아이디는 어떻게 처리하나요", 11),
]


def embed(texts, model):
    r = requests.post(URL, json={"model": model, "input": texts}, timeout=300).json()
    v = np.array(r["embeddings"], dtype=float)
    return v / np.linalg.norm(v, axis=1, keepdims=True)


def evaluate(model, doc_prefix, query_prefix):
    D = embed([doc_prefix + d for d in DOCS], model)
    Q = embed([query_prefix + q for q, _ in QUERIES], model)
    S = Q @ D.T
    top1 = top3 = 0
    right, wrong = [], []
    for i, (_, gold) in enumerate(QUERIES):
        order = np.argsort(-S[i])
        top1 += order[0] == gold
        top3 += gold in order[:3]
        right.append(S[i, gold])
        wrong.extend(S[i, j] for j in range(len(DOCS)) if j != gold)
    return top1, top3, np.mean(right), np.mean(wrong), min(right), max(wrong), S


NP = "search_document: ", "search_query: "          # nomic-embed-text 가 권하는 접두어
CASES = [("nomic-embed-text", "접두어 없음", "", ""), ("nomic-embed-text", "접두어 사용", *NP), ("bge-m3", "접두어 없음", "", "")]

print("## 1. 모델과 접두어 비교(문서 12개, 질문 12개)")
print(f"  {'모델':<18}{'설정':<12}{'1등 정답':>8}{'3등 안':>8}{'정답 평균점수':>14}{'오답 평균점수':>14}{'점수 차':>9}")
res = {}
for model, label, dp, qp in CASES:
    t1, t3, mr, mw, mn, mx, S = evaluate(model, dp, qp)
    res[(model, label)] = (mn, mx, S, dp, qp)
    print(f"  {model:<18}{label:<12}{t1:>6}/12{t3:>6}/12{mr:>14.3f}{mw:>14.3f}{mr - mw:>9.3f}")

print("\n## 2. 임계값: '이 점수 이상이면 찾았다'로 정할 때(모델마다 점수 분포가 다르다)")
for key in (("nomic-embed-text", "접두어 사용"), ("bge-m3", "접두어 없음")):
    mn, mx, S, _, _ = res[key]
    print(f"  [{key[0]}] 정답 점수 가장 낮은 값 {mn:.3f}, 오답 점수 가장 높은 값 {mx:.3f}")
    for th in (0.5, 0.6, 0.7):
        hits = sum(1 for i, (_, g) in enumerate(QUERIES) if S[i, g] >= th)
        fp = sum(1 for i, (_, g) in enumerate(QUERIES) for j in range(len(DOCS)) if j != g and S[i, j] >= th)
        print(f"    임계값 {th}: 정답 중 통과 {hits}/12, 오답 중 잘못 통과 {fp}/{12 * 11}")

print("\n## 3. 문서와 전혀 상관없는 질문의 가장 높은 점수")
for model, dp, qp in (("nomic-embed-text", *NP), ("bge-m3", "", "")):
    D = embed([dp + d for d in DOCS], model)
    for q in ("오늘 점심 메뉴 추천해 주세요", "축구 경기 결과 알려 줘", "How do I bake bread?"):
        s_ = (embed([qp + q], model) @ D.T)[0]
        print(f"  {model:<18}{q:<22} {s_.max():.3f} (문서 {s_.argmax()}번)")
