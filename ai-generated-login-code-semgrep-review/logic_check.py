"""수정본 B와 C에서 Semgrep이 보지 못하는 논리 결함을 Flask 테스트 클라이언트로 직접 확인합니다."""
import os
import tempfile

os.environ["SECRET_KEY"] = "test-only-key"
os.chdir(tempfile.mkdtemp())

import fixed_b
import fixed_c

fixed_b.init_db()
cb = fixed_b.app.test_client()
cb.post("/register", data={"username": "alice", "password": "alice-pw-1"})
print("[B] 없는 계정      :", cb.post("/login", data={"username": "nobody", "password": "x"}).get_data(as_text=True))
print("[B] 틀린 비밀번호  :", cb.post("/login", data={"username": "alice", "password": "x"}).get_data(as_text=True))
codes = [cb.post("/login", data={"username": "alice", "password": f"guess{i}"}).status_code for i in range(30)]
print("[B] 연속 30회 실패 :", set(codes), "(잠금이나 지연 없이 계속 401)")
print("[B] 그 뒤 올바른 비밀번호:", cb.post("/login", data={"username": "alice", "password": "alice-pw-1"}).get_data(as_text=True))

fixed_c.init_db()
cc = fixed_c.app.test_client()
cc.post("/login", data={"username": "guest", "password": "guest-pw-1"}, base_url="https://localhost")
r = cc.get("/admin", base_url="https://localhost")
print("[C] 일반 사용자 guest 의 /admin :", r.status_code, r.get_data(as_text=True))
