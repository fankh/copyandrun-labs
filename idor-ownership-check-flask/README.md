# Flask에서 소유자 검사로 IDOR 막기

로그인만 확인하고 주문의 주인은 확인하지 않는 Flask API가 남의 주문을 돌려주는 것을 pytest 한 건으로 확인합니다. 쿼리에 소유자 조건을 넣고 번호를 받는 엔드포인트에 같은 데코레이터를 붙인 뒤, 사용자와 역할 조합 표로 회귀 테스트를 만듭니다.

글: https://copyandrun.com/blog/idor-ownership-check-flask/

## 파일

- `app.py`
- `base.py`
- `index.html`
- `requirements.txt`
- `test_orders.py`
- `test_vuln.py`
- `vuln_app.py`

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
