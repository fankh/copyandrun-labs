"""ISMS-P 기술 점검 일부를 자동으로 확인해 표로 만드는 참고용 스크립트입니다.

인증 심사를 대신하지 않으며 법적 적합성을 판단하지 않습니다. 기준값은 이 연습용 값입니다.
사용법: python3 check.py [--allow ops] [--min-days 365] [--host 127.0.0.1] [--port 443]
결과: 양호 / 취약 / 수동확인. 취약이 하나라도 있으면 종료 코드 1.
"""
import argparse
import re
import socket
import stat
import subprocess
import sys
from pathlib import Path

LOGIN_SHELL_SKIP = ("nologin", "false")


def read_passwd():
    rows = []
    for line in Path("/etc/passwd").read_text().splitlines():
        p = line.split(":")
        rows.append({"name": p[0], "uid": int(p[2]), "shell": p[6]})
    shadow = {}
    for line in Path("/etc/shadow").read_text().splitlines():
        p = line.split(":")
        shadow[p[0]] = p[1]
    return rows, shadow


def check_accounts(allow):
    rows, shadow = read_passwd()
    bad = []
    for r in rows:
        if r["uid"] < 1000 or r["uid"] == 65534:
            continue
        if r["shell"].endswith(LOGIN_SHELL_SKIP):
            continue
        locked = shadow.get(r["name"], "!")[:1] in ("!", "*")
        if r["name"] not in allow and not locked:
            bad.append(r["name"])
    if bad:
        return "취약", "승인 목록 밖의 로그인 가능 계정: " + ", ".join(bad)
    return "양호", "승인 목록 밖의 로그인 가능 계정 없음"


def check_empty_password():
    _, shadow = read_passwd()
    bad = [n for n, h in shadow.items() if h == ""]
    if bad:
        return "취약", "비밀번호가 빈 계정: " + ", ".join(bad)
    return "양호", "비밀번호가 빈 계정 없음"


def check_max_days():
    m = re.search(r"^PASS_MAX_DAYS\s+(\d+)", Path("/etc/login.defs").read_text(), re.M)
    if not m:
        return "수동확인", "PASS_MAX_DAYS 설정 없음"
    default = int(m.group(1))
    # login.defs 의 값은 새로 만드는 계정의 기본값이므로, 기존 계정은 shadow 5번째 칸(최대 사용 일수)을 따로 읽습니다.
    rows, _ = read_passwd()
    per = {}
    for line in Path("/etc/shadow").read_text().splitlines():
        p = line.split(":")
        per[p[0]] = p[4]
    bad, parts = [], []
    for r in rows:
        if r["uid"] < 1000 or r["uid"] == 65534 or r["shell"].endswith(LOGIN_SHELL_SKIP):
            continue
        raw = per.get(r["name"], "")
        days = int(raw) if raw.isdigit() else 99999
        parts.append(f"{r['name']}={days}")
        if days > 90:
            bad.append(r["name"])
    detail = f"신규 계정 기본값 {default}, 로그인 계정별 " + (", ".join(parts) or "없음") + " (기준 90일 이하)"
    return ("양호" if default <= 90 and not bad else "취약"), detail


def check_minlen():
    f = Path("/etc/security/pwquality.conf")
    if not f.exists():
        return "취약", "pwquality.conf 없음, 최소 길이 설정 없음"
    m = re.search(r"^\s*minlen\s*=\s*(\d+)", f.read_text(), re.M)
    if not m:
        return "취약", "minlen 설정 없음"
    n = int(m.group(1))
    return ("양호" if n >= 8 else "취약"), f"minlen={n} (기준 8 이상, PAM 적용은 수동확인)"


def check_log_perm(path="/var/log/nginx/access.log"):
    f = Path(path)
    if not f.exists():
        return "수동확인", "접근 로그 파일 없음"
    mode = stat.S_IMODE(f.stat().st_mode)
    ok = mode & 0o137 == 0
    return ("양호" if ok else "취약"), f"mode={oct(mode)[2:]} (기준 640 이하)"


def check_log_keep(min_days):
    f = Path("/etc/logrotate.d/nginx")
    if not f.exists():
        return "수동확인", "logrotate 설정 없음"
    t = f.read_text()
    unit = {"daily": 1, "weekly": 7, "monthly": 30}
    per = next((v for k, v in unit.items() if re.search(rf"^\s*{k}\b", t, re.M)), None)
    m = re.search(r"^\s*rotate\s+(\d+)", t, re.M)
    if per is None or not m:
        return "수동확인", "주기나 rotate 값을 읽지 못함"
    days = per * int(m.group(1))
    return ("양호" if days >= min_days else "취약"), f"약 {days}일 보관 (기준 {min_days}일 이상)"


def probe(host, port, flag):
    p = subprocess.run(
        ["openssl", "s_client", flag, "-cipher", "DEFAULT:@SECLEVEL=0", "-connect", f"{host}:{port}"],
        input="", capture_output=True, text=True, timeout=15)
    return "Cipher is" in p.stdout and "Cipher is (NONE)" not in p.stdout


def check_tls(host, port):
    try:
        socket.create_connection((host, port), 3).close()
    except OSError:
        return "수동확인", f"{host}:{port} 에 연결하지 못함"
    old = [name for flag, name in (("-tls1", "TLS 1.0"), ("-tls1_1", "TLS 1.1")) if probe(host, port, flag)]
    new = [name for flag, name in (("-tls1_2", "TLS 1.2"), ("-tls1_3", "TLS 1.3")) if probe(host, port, flag)]
    if old:
        return "취약", "허용: " + ", ".join(old + new)
    return "양호", "허용: " + ", ".join(new) + " (1.0, 1.1 거절)"


def check_data(folder="/srv/data"):
    phone = re.compile(rb"01\d-\d{3,4}-\d{4}")
    plain, enc = [], []
    for f in sorted(Path(folder).glob("*")):
        head = f.read_bytes()
        if head.startswith(b"Salted__"):
            enc.append(f.name)
        elif phone.search(head):
            plain.append(f.name)
    if plain:
        return "취약", "전화번호가 평문인 파일: " + ", ".join(plain)
    if enc:
        return "양호", "암호화 형식 파일: " + ", ".join(enc)
    return "수동확인", "점검 대상 파일 없음"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--allow", default="ops", help="승인된 로그인 계정(쉼표)")
    ap.add_argument("--min-days", type=int, default=365)
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=443)
    a = ap.parse_args()
    allow = set(a.allow.split(","))
    items = [
        ("계정 관리", "불필요 계정", "passwd, shadow 에서 승인 밖 로그인 계정", check_accounts(allow)),
        ("계정 관리", "빈 비밀번호", "shadow 의 비밀번호 칸", check_empty_password()),
        ("계정 관리", "비밀번호 만료", "login.defs 기본값과 shadow 계정별 최대 일수", check_max_days()),
        ("계정 관리", "비밀번호 길이", "pwquality.conf minlen", check_minlen()),
        ("접근 로그", "로그 파일 권한", "access.log 파일 모드", check_log_perm()),
        ("접근 로그", "로그 보관 기간", "logrotate 주기 x rotate", check_log_keep(a.min_days)),
        ("전송 암호화", "TLS 버전", "openssl s_client 로 버전별 접속", check_tls(a.host, a.port)),
        ("저장 암호화", "저장 파일", "/srv/data 파일 내용과 헤더", check_data()),
        ("저장 암호화", "디스크 암호화", "컨테이너 안에서는 확인 불가", ("수동확인", "호스트 볼륨 암호화는 담당자가 별도 확인")),
    ]
    head = ("구분", "항목", "확인 방법", "결과", "근거")
    rows = [(g, i, m, r[0], r[1]) for g, i, m, r in items]
    print("| " + " | ".join(head) + " |")
    print("|" + "---|" * 5)
    for r in rows:
        print("| " + " | ".join(r) + " |")
    count = {k: sum(1 for r in rows if r[3] == k) for k in ("양호", "취약", "수동확인")}
    print(f"\n양호 {count['양호']}  취약 {count['취약']}  수동확인 {count['수동확인']}")
    sys.exit(1 if count["취약"] else 0)


if __name__ == "__main__":
    main()
