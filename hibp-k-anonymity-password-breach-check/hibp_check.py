"""Pwned Passwords range API 로 비밀번호 유출 여부를 k-익명성 방식으로 확인합니다.

사용법:
  python hibp_check.py                      비밀번호를 화면에 보이지 않게 입력받습니다(권장)
  python hibp_check.py --password 시험값    연습용 값만 씁니다. 실제 비밀번호는 명령행에 쓰지 않습니다
  python hibp_check.py --random             방금 무작위로 만든 긴 문자열을 확인합니다
  옵션: --padding (Add-Padding 헤더 사용), --show (서버로 나가는 요청 주소만 출력)
"""
import argparse
import getpass
import hashlib
import secrets
import sys
import urllib.request

API = "https://api.pwnedpasswords.com/range/"


def sha1_upper(password: str) -> str:
    return hashlib.sha1(password.encode("utf-8")).hexdigest().upper()


def fetch_range(prefix: str, padding: bool = False) -> str:
    headers = {"User-Agent": "copyandrun-hibp-demo"}
    if padding:
        headers["Add-Padding"] = "true"
    req = urllib.request.Request(API + prefix, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as res:
        return res.read().decode("utf-8")


def find_count(body: str, suffix: str) -> int:
    """응답의 'SUFFIX:COUNT' 줄에서 내 나머지 35자리를 로컬에서 찾습니다."""
    for line in body.splitlines():
        got, _, count = line.strip().partition(":")
        if got == suffix:
            return int(count)
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--password")
    ap.add_argument("--random", action="store_true")
    ap.add_argument("--padding", action="store_true")
    ap.add_argument("--show", action="store_true")
    a = ap.parse_args()

    if a.random:
        password = secrets.token_urlsafe(24)
        print(f"무작위 시험값: {password}")
    elif a.password is not None:
        password = a.password
    else:
        password = getpass.getpass("확인할 비밀번호(입력은 보이지 않습니다): ")

    digest = sha1_upper(password)
    prefix, suffix = digest[:5], digest[5:]
    print(f"SHA-1 전체 해시 : {digest}")
    print(f"서버로 보내는 값: {prefix}  (앞 5자리)")
    print(f"로컬에만 두는 값: {suffix}  ({len(suffix)}자리)")
    if a.show:
        print("요청 주소:", API + prefix)
        return

    body = fetch_range(prefix, a.padding)
    lines = body.splitlines()
    zero = sum(1 for ln in lines if ln.strip().endswith(":0"))
    print(f"응답 줄 수: {len(lines)} (그중 count 0 인 채움 줄 {zero})")
    n = find_count(body, suffix)
    if n:
        print(f"결과: 유출 목록에서 {n:,}회 발견됨. 이 비밀번호는 쓰지 않습니다.")
    else:
        print("결과: 목록에서 찾지 못함. 안전하다는 뜻은 아닙니다.")
    sys.exit(1 if n else 0)


if __name__ == "__main__":
    main()
