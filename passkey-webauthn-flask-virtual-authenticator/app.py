"""패스키(WebAuthn) 등록과 로그인을 붙인 Flask 연습 앱. 저장소는 메모리라 재시작하면 사라집니다."""
from flask import Flask, jsonify, request, session
from webauthn import (
    generate_authentication_options,
    generate_registration_options,
    options_to_json,
    verify_authentication_response,
    verify_registration_response,
)
from webauthn.helpers import base64url_to_bytes, bytes_to_base64url
from webauthn.helpers.structs import (
    PublicKeyCredentialDescriptor,
    UserVerificationRequirement,
)

PORT = 5050
RP_ID = "localhost"                      # 도메인만. 포트와 스킴은 넣지 않습니다.
RP_NAME = "Passkey Lab"
EXPECTED_ORIGIN = f"http://localhost:{PORT}"   # 서버가 믿는 유일한 origin

app = Flask(__name__)
app.secret_key = "lab-only-secret-key"   # 실습용 고정값. 운영에서는 환경 변수로 주입합니다.

# 비밀번호 로그인과 비교하려고 비밀번호 계정도 하나 둡니다. 실습용 평문입니다.
USERS = {"alice": {"password": "Summer2024!", "id": b"user-alice-0001", "creds": {}}}
EVENTS = []          # 화면에 보여 줄 서버 쪽 판정 기록


def log(kind, ok, detail):
    EVENTS.append({"kind": kind, "ok": ok, "detail": detail})
    del EVENTS[:-12]


def fail(kind, exc):
    log(kind, False, f"{type(exc).__name__}: {exc}")
    return jsonify(ok=False, error=str(exc)), 400


@app.get("/")
def index():
    return PAGE


@app.get("/state")
def state():
    u = USERS["alice"]
    return jsonify(
        user=session.get("user"),
        via=session.get("via"),
        host=request.host,
        creds=[{"id": cid[:12] + "...", "sign_count": c["sign_count"]} for cid, c in u["creds"].items()],
        events=EVENTS,
    )


@app.post("/pw-login")
def pw_login():
    data = request.get_json()
    user = USERS.get(data.get("username"))
    if user and user["password"] == data.get("password"):
        session.clear()
        session["user"], session["via"] = data["username"], "password"
        log("password", True, f"비밀번호 로그인 허용 (접속 주소 {request.host})")
        return jsonify(ok=True)
    log("password", False, "비밀번호 불일치")
    return jsonify(ok=False), 401


@app.post("/register/options")
def register_options():
    if session.get("via") != "password":
        return jsonify(ok=False, error="먼저 비밀번호로 로그인하세요"), 401
    user = USERS[session["user"]]
    opts = generate_registration_options(
        rp_id=RP_ID,
        rp_name=RP_NAME,
        user_id=user["id"],
        user_name=session["user"],
        exclude_credentials=[
            PublicKeyCredentialDescriptor(id=base64url_to_bytes(cid)) for cid in user["creds"]
        ],
    )
    session["challenge"] = bytes_to_base64url(opts.challenge)   # 서버가 발급한 값을 저장
    return app.response_class(options_to_json(opts), mimetype="application/json")


@app.post("/register/verify")
def register_verify():
    challenge = session.pop("challenge", None)       # 꺼내면서 지웁니다. 1회용입니다.
    if challenge is None:
        return fail("register", ValueError("발급된 챌린지가 없거나 이미 사용했습니다"))
    user = USERS[session["user"]]
    try:
        v = verify_registration_response(
            credential=request.get_json(),
            expected_challenge=base64url_to_bytes(challenge),
            expected_rp_id=RP_ID,
            expected_origin=EXPECTED_ORIGIN,
        )
    except Exception as exc:
        return fail("register", exc)
    user["creds"][bytes_to_base64url(v.credential_id)] = {
        "public_key": v.credential_public_key,
        "sign_count": v.sign_count,
    }
    log("register", True, f"패스키 등록 (공개키 {len(v.credential_public_key)}바이트 저장, 개인키는 서버에 없음)")
    return jsonify(ok=True)


@app.post("/login/options")
def login_options():
    user = USERS["alice"]
    opts = generate_authentication_options(
        rp_id=RP_ID,
        allow_credentials=[
            PublicKeyCredentialDescriptor(id=base64url_to_bytes(cid)) for cid in user["creds"]
        ],
        user_verification=UserVerificationRequirement.PREFERRED,
    )
    session["challenge"] = bytes_to_base64url(opts.challenge)
    return app.response_class(options_to_json(opts), mimetype="application/json")


@app.post("/login/verify")
def login_verify():
    challenge = session.pop("challenge", None)       # 1회용
    if challenge is None:
        return fail("login", ValueError("발급된 챌린지가 없거나 이미 사용했습니다"))
    body = request.get_json()
    cred = USERS["alice"]["creds"].get(body.get("id"))
    if cred is None:
        return fail("login", ValueError("등록되지 않은 패스키입니다"))
    try:
        v = verify_authentication_response(
            credential=body,
            expected_challenge=base64url_to_bytes(challenge),
            expected_rp_id=RP_ID,
            expected_origin=EXPECTED_ORIGIN,         # 다른 origin 에서 만든 서명은 여기서 거부
            credential_public_key=cred["public_key"],
            credential_current_sign_count=cred["sign_count"],
        )
    except Exception as exc:
        return fail("login", exc)
    cred["sign_count"] = v.new_sign_count            # 카운터를 올려 저장
    session.clear()
    session["user"], session["via"] = "alice", "passkey"
    log("login", True, f"패스키 로그인 허용 (서명 카운터 {v.new_sign_count})")
    return jsonify(ok=True, sign_count=v.new_sign_count)


@app.post("/logout")
def logout():
    session.clear()
    return jsonify(ok=True)


PAGE = """<!doctype html><meta charset="utf-8"><title>Passkey Lab</title>
<style>
body{font-family:'Malgun Gothic',sans-serif;margin:28px;color:#222;max-width:900px}
h1{margin:0 0 4px}.host{color:#555;margin-bottom:16px}
.card{border:1px solid #ccd;border-radius:8px;padding:14px 18px;margin:12px 0}
button{padding:8px 14px;margin-right:8px;font-size:15px;cursor:pointer}
input{padding:7px;font-size:15px;margin-right:8px}
#me{font-weight:700;padding:10px 14px;border-radius:8px;background:#eef1f5}
#me.in{background:#dff5e1;color:#14692a}
pre{background:#101820;color:#d8e2ea;padding:10px 12px;border-radius:6px;font-size:13px;white-space:pre-wrap;margin:8px 0 0}
.bad{color:#ff8a8a}.good{color:#8be59b}
</style>
<h1>Passkey Lab</h1>
<div class="host">접속 주소: <b id="host"></b> (서버가 믿는 origin: http://localhost:5050)</div>
<div id="me"></div>
<div class="card"><b>1. 비밀번호 로그인</b><br>
<input id="u" value="alice" size="8"><input id="p" type="password" value="Summer2024!" size="12">
<button onclick="pwLogin()">비밀번호로 로그인</button></div>
<div class="card"><b>2. 패스키 등록</b> (비밀번호로 로그인한 뒤)<br>
<button onclick="reg()">패스키 만들기</button></div>
<div class="card"><b>3. 패스키 로그인</b><br>
<button onclick="login()">패스키로 로그인</button>
<button onclick="replay()">같은 응답 다시 보내기</button>
<button onclick="out_()">로그아웃</button></div>
<div class="card"><b>서버 판정 기록</b><pre id="ev"></pre></div>
<script>
const J = (u, b) => fetch(u, {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(b || {})});
let last = null;
async function refresh() {
  const s = await (await fetch('/state')).json();
  document.getElementById('host').textContent = location.origin;
  const me = document.getElementById('me');
  me.className = s.user ? 'in' : '';
  const creds = s.creds.map(c => c.id + ' 카운터=' + c.sign_count).join(', ') || '없음';
  me.textContent = (s.user ? '로그인됨: ' + s.user + ' (' + s.via + ')' : '로그아웃 상태') + '   |   등록된 패스키: ' + creds;
  document.getElementById('ev').innerHTML = s.events.map(e =>
    '<span class="' + (e.ok ? 'good' : 'bad') + '">' + (e.ok ? '허용 ' : '거부 ') + e.kind + '</span>  ' + e.detail.replace(/</g, '&lt;')).join('\\n');
}
async function pwLogin() { await J('/pw-login', {username: u.value, password: p.value}); refresh(); }
async function reg() {
  const o = await (await J('/register/options')).json();
  if (o.error) { alert(o.error); return; }
  const cred = await navigator.credentials.create({publicKey: PublicKeyCredential.parseCreationOptionsFromJSON(o)});
  await J('/register/verify', cred.toJSON()); refresh();
}
async function login() {
  const o = await (await J('/login/options')).json();
  let cred;
  try { cred = await navigator.credentials.get({publicKey: PublicKeyCredential.parseRequestOptionsFromJSON(o)}); }
  catch (e) { document.getElementById('ev').textContent = '브라우저가 거부: ' + e.name + ' ' + e.message; return; }
  last = cred.toJSON();
  await J('/login/verify', last); refresh();
}
async function replay() { if (last) { await J('/login/verify', last); refresh(); } }
async function out_() { await J('/logout'); refresh(); }
refresh();
</script>"""


if __name__ == "__main__":
    # evil.localhost 로도 접속해 볼 수 있게 localhost 이름 전체에서 받습니다.
    app.run(host="127.0.0.1", port=PORT)
