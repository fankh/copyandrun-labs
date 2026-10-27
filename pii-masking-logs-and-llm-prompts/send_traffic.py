"""앱에 가짜 개인정보가 담긴 요청을 보냅니다. 값은 모두 실습용으로 만든 가짜입니다."""
import json
import sys
import urllib.error
import urllib.parse
import urllib.request

APP = "http://127.0.0.1:5792"
LLM = "http://127.0.0.1:5793"
DOMAIN = "example.com"  # 예약된 예시 도메인


def call(method, url, body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data, {"Content-Type": "application/json"}, method=method)
    try:
        with urllib.request.urlopen(req) as res:
            return res.status
    except urllib.error.HTTPError as exc:
        return exc.code


MODE = sys.argv[1]  # before 또는 after: 해당 구분의 수신 기록만 비우고 시작합니다
call("POST", f"{LLM}/reset?mode={MODE}")
requests = [
    ("POST", "/signup", {"name": "테스트고객1", "rrn": "900101-1234567", "phone": "010-1234-5678", "email": f"tester1@{DOMAIN}"}),
    ("POST", "/signup", {"name": "테스트고객2", "rrn": "8503152345678", "phone": "01055550101", "email": f"tester2@{DOMAIN}"}),
    ("POST", "/payment", {"card": "4111 1111 1111 1111", "amount": 12000, "memo": "주문 ORD-2610271234567 건"}),
    ("POST", "/payment", {"card": "5555-5555-5555-4444", "amount": 8500, "memo": "송장 1234-5678-9012-3456 배송 문의"}),
    ("POST", "/chat", {"message": "제 주민번호는 900101-1234567 이고 연락처는 010-1234-5678 입니다. 환불 계좌 등록을 도와주세요."}),
    ("POST", "/chat", {"message": f"카드 4111 1111 1111 1111 결제가 두 번 됐습니다. 결과는 tester1@{DOMAIN} 으로 알려 주세요."}),
    ("GET", "/lookup?" + urllib.parse.urlencode({"phone": "010-9999-0000"}), None),
]
for method, path, body in requests:
    print(call(method, APP + path, body), method, path.split("?")[0])
