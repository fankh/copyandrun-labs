# 패스키(WebAuthn)를 Flask에 붙이기: 가상 인증기로 등록과 로그인 확인

비밀번호 재사용과 피싱 중계로 계정이 넘어가는 것을 재현한 뒤, py_webauthn으로 패스키 등록과 로그인을 Flask에 붙입니다. 크롬의 가상 인증기를 CDP로 켜서 등록, 로그인, 챌린지 1회성, origin 검증, 서명 카운터를 확인하고, 복구 경로와 동기화 패스키 같은 한계까지 정리합니다.

## 링크

- 글: [https://copyandrun.com/blog/passkey-webauthn-flask-virtual-authenticator/](https://copyandrun.com/blog/passkey-webauthn-flask-virtual-authenticator/)
- 한 번에 받기: [passkey-webauthn-flask-virtual-authenticator.zip](https://copyandrun.com/code-zip/passkey-webauthn-flask-virtual-authenticator.zip)
- GitHub 폴더: [copyandrun-labs/passkey-webauthn-flask-virtual-authenticator](https://github.com/fankh/copyandrun-labs/tree/main/passkey-webauthn-flask-virtual-authenticator)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `app.py` | <a href="https://fankh.github.io/copyandrun-labs/passkey-webauthn-flask-virtual-authenticator/app.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/passkey-webauthn-flask-virtual-authenticator/app.py) |
| `drive.py` | <a href="https://fankh.github.io/copyandrun-labs/passkey-webauthn-flask-virtual-authenticator/drive.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/passkey-webauthn-flask-virtual-authenticator/drive.py) |
| `phish.py` | <a href="https://fankh.github.io/copyandrun-labs/passkey-webauthn-flask-virtual-authenticator/phish.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/passkey-webauthn-flask-virtual-authenticator/phish.py) |
| `requirements.txt` | <a href="https://fankh.github.io/copyandrun-labs/passkey-webauthn-flask-virtual-authenticator/requirements.txt" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/passkey-webauthn-flask-virtual-authenticator/requirements.txt) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
