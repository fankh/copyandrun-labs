#!/usr/bin/env python3
"""kubescape 의 JSON 결과를 요약하고, 반드시 통과해야 하는 통제가 실패하면 종료 코드 1 로 끝낸다.
사용: python ks_summary.py weak.json [--list]   (파일 하나씩 부르면 그 파일의 판정이 종료 코드가 된다)"""
import json
import sys

sys.stdout.reconfigure(encoding="utf-8")

# 파드 명세에서 직접 고칠 수 있는 통제만 게이트로 삼는다(이미지 서명, 네트워크 정책 등은 제외).
MUST = {
    "C-0013": "루트가 아닌 사용자로 실행",
    "C-0016": "권한 상승 금지",
    "C-0017": "읽기 전용 루트 파일시스템",
    "C-0057": "privileged 금지",
    "C-0034": "서비스 어카운트 토큰 자동 마운트 끔",
    "C-0210": "seccomp 프로파일 지정",
    "C-0009": "리소스 제한",
}
worst = 0
show_list = "--list" in sys.argv
for path in [a for a in sys.argv[1:] if not a.startswith("--")]:
    s = json.load(open(path, encoding="utf-8"))["summaryDetails"]
    failed = {cid: c for cid, c in s["controls"].items() if c["ResourceCounters"]["failedResources"]}
    by_sev = {}
    for c in failed.values():
        by_sev[c["severity"]] = by_sev.get(c["severity"], 0) + 1
    print(f"== {path}")
    print(f"  통제 {len(s['controls'])}개 중 실패 {len(failed)}개, 위험 점수 {s['score']:.1f}, 준수 점수 {s['complianceScore']:.1f}")
    print("  심각도별 실패: " + ", ".join(f"{k} {by_sev[k]}" for k in ("High", "Medium", "Low") if k in by_sev))
    if show_list:
        for cid, c in sorted(failed.items()):
            print(f"  남은 실패  {cid}  {c['severity']:<6}  {c['name']}")
    miss = [cid for cid in MUST if cid in failed]
    for cid in MUST:
        print(f"  {'실패' if cid in failed else '통과'}  {cid}  {MUST[cid]}")
    if miss:
        worst = 1
print("종료 코드 기준: 필수 통제가 하나라도 실패하면 1")
sys.exit(worst)
