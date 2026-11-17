"""응답 필드 점검 게이트입니다. 표준 라이브러리만 씁니다.

사용: python check_fields.py http://127.0.0.1:8000
엔드포인트마다 허용 필드 목록과 대조하고, 민감해 보이는 키 이름이 있으면 함께 보고합니다.
위반이 하나라도 있으면 종료 코드 1을 돌려줍니다.
"""
import json
import re
import sys
import urllib.request

CALLER = "alice"
# (경로, 허용 필드). 목록 응답은 항목마다 같은 허용 필드를 적용합니다.
CHECKS = [
    ("/users/me", {"username", "display_name", "team", "email", "phone", "role"}),
    ("/users/dana", {"username", "display_name", "team"}),
    ("/users", {"username", "display_name", "team"}),
]
SENSITIVE = re.compile(r"password|hash|secret|token|api_?key|internal|note", re.I)


def fetch(base, path):
    req = urllib.request.Request(base + path, headers={"X-User": CALLER})
    with urllib.request.urlopen(req, timeout=5) as r:
        return json.load(r)


def main():
    base = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else "http://127.0.0.1:8000"
    bad = 0
    for path, allowed in CHECKS:
        data = fetch(base, path)
        items = data if isinstance(data, list) else [data]
        extra = sorted({k for item in items for k in item} - allowed)
        flagged = [k for k in extra if SENSITIVE.search(k)]
        if extra:
            bad += 1
            print(f"FAIL {path}: 허용 목록에 없는 필드 {extra} (민감 키 이름: {flagged or '없음'})")
        else:
            print(f"PASS {path}: 필드 {len(allowed)}개 이내")
    print("결과:", "실패 %d건" % bad if bad else "모두 통과")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
