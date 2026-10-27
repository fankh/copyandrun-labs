# XSS 막기: 출력 이스케이프와 CSP를 Flask에 적용하고 브라우저에서 확인

게시판 앱에서 저장형 XSS를 일으켜 보고, 자동 이스케이프와 nonce CSP 헤더, HttpOnly·SameSite 쿠키로 고친 뒤 개발자 도구의 Console과 Network 탭에서 막힌 것을 확인합니다.

글: https://copyandrun.com/blog/xss-output-escaping-and-csp-flask/

## 파일

- `app.py`
- `app_csp.py`
- `app_fixed.py`
- `requirements.txt`

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
