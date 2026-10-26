# 작은 Flask 서비스를 직접 공격하고 한 줄씩 고치기

빈 폴더에서 Flask 게시판을 직접 띄우고 로그인·다운로드·게시판 기능을 차례로 뚫어 봅니다. 뚫은 지점을 그대로 한 줄씩 고치면서 왜 그 한 줄이 공격을 막는지 눈으로 확인합니다.

글: https://copyandrun.com/blog/flask-attack-and-fix-own-app/

## 파일

- `app.py`
- `app_fixed.py`
- `check_stolen.py`
- `init_db.py`
- `requirements.txt`

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
