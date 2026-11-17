# XSS 막기: 출력 이스케이프와 CSP를 Flask에 적용하고 브라우저에서 확인

게시판 앱에서 저장형 XSS를 일으켜 보고, 자동 이스케이프와 nonce CSP 헤더, HttpOnly·SameSite 쿠키로 고친 뒤 개발자 도구의 Console과 Network 탭에서 막힌 것을 확인합니다.

## 링크

- 글: [https://copyandrun.com/blog/xss-output-escaping-and-csp-flask/](https://copyandrun.com/blog/xss-output-escaping-and-csp-flask/)
- 한 번에 받기: [xss-output-escaping-and-csp-flask.zip](https://copyandrun.com/code-zip/xss-output-escaping-and-csp-flask.zip)
- GitHub 폴더: [copyandrun-labs/xss-output-escaping-and-csp-flask](https://github.com/fankh/copyandrun-labs/tree/main/xss-output-escaping-and-csp-flask)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `app.py` | <a href="https://fankh.github.io/copyandrun-labs/xss-output-escaping-and-csp-flask/app.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/xss-output-escaping-and-csp-flask/app.py) |
| `app_csp.py` | <a href="https://fankh.github.io/copyandrun-labs/xss-output-escaping-and-csp-flask/app_csp.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/xss-output-escaping-and-csp-flask/app_csp.py) |
| `app_fixed.py` | <a href="https://fankh.github.io/copyandrun-labs/xss-output-escaping-and-csp-flask/app_fixed.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/xss-output-escaping-and-csp-flask/app_fixed.py) |
| `requirements.txt` | <a href="https://fankh.github.io/copyandrun-labs/xss-output-escaping-and-csp-flask/requirements.txt" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/xss-output-escaping-and-csp-flask/requirements.txt) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
