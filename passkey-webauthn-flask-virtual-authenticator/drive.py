"""가상 인증기로 등록, 로그인, 재전송, 피싱 주소 접속을 자동으로 확인합니다.

사용법: python app.py 와 python phish.py 를 각각 띄운 뒤 다른 터미널에서
    python drive.py            (결과 출력만)
    python drive.py shots      (shots 폴더에 화면도 저장)
환경 변수 CHROME_PATH 로 Chrome 실행 파일을 지정할 수 있습니다.
"""
import os
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

CHROME = os.environ.get("CHROME_PATH", r"C:\Program Files\Google\Chrome\Application\chrome.exe")
SHOTS = Path(sys.argv[1]) if len(sys.argv) > 1 else None
GOOD = "http://localhost:5050/"
RELAY = "http://localhost:5051/"          # phish.py 가 띄우는 중계 서버
EVIL = "http://evil.localhost:5050/"      # 다른 도메인에서 접속하는 경우


def shot(page, name):
    if SHOTS:
        SHOTS.mkdir(parents=True, exist_ok=True)
        page.screenshot(path=str(SHOTS / name))


def status(page):
    page.wait_for_timeout(500)
    me = page.inner_text("#me")
    ev = page.inner_text("#ev").strip().splitlines()
    return me, ev[-1] if ev else ""


def virtual_authenticator(context, page):
    cdp = context.new_cdp_session(page)
    cdp.send("WebAuthn.enable")
    cdp.send("WebAuthn.addVirtualAuthenticator", {"options": {
        "protocol": "ctap2", "transport": "internal",
        "hasResidentKey": True, "hasUserVerification": True,
        "isUserVerified": True, "automaticPresenceSimulation": True,
    }})
    return cdp


with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=CHROME, headless=True)

    # 1. 정상 주소: 등록, 로그인, 재전송
    ctx = browser.new_context(viewport={"width": 980, "height": 760})
    page = ctx.new_page()
    virtual_authenticator(ctx, page)
    page.goto(GOOD)
    page.wait_for_timeout(500)
    shot(page, "01-start.png")

    page.click("text=비밀번호로 로그인")
    print("비밀번호 로그인  ", *status(page))
    page.click("text=패스키 만들기")
    me, last = status(page)
    print("패스키 등록     ", me, "|", last)
    shot(page, "02-registered.png")

    page.click("text=로그아웃")
    page.click("text=패스키로 로그인")
    me, last = status(page)
    print("패스키 로그인 1 ", me, "|", last)
    page.click("text=로그아웃")
    page.click("text=패스키로 로그인")
    me, last = status(page)
    print("패스키 로그인 2 ", me, "|", last)
    shot(page, "03-login-ok.png")

    page.click("text=같은 응답 다시 보내기")
    me, last = status(page)
    print("같은 응답 재전송", me, "|", last)
    shot(page, "04-replay.png")

    # 2. 피싱 중계 서버(phish.py, 5051): 같은 탭, 같은 가상 인증기에서 주소만 바꿉니다.
    page.goto(RELAY)
    page.click("text=비밀번호로 로그인")
    me, last = status(page)
    print("중계 주소 비밀번호", me, "|", last)
    shot(page, "05-phish-password.png")
    page.click("text=로그아웃")
    page.click("text=패스키로 로그인")
    me, last = status(page)
    print("중계 주소 패스키 ", me, "|", last)
    shot(page, "06-phish-passkey.png")

    # 3. 가짜 도메인(evil.localhost): 브라우저가 서명 자체를 만들지 않습니다.
    page.goto(EVIL)
    page.click("text=패스키로 로그인")
    me, last = status(page)
    print("가짜 도메인 패스키", last)
    shot(page, "07-phish-browser.png")
    ctx.close()
    browser.close()
