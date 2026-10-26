# Flask에서 SQL 쿼리를 파라미터 바인딩으로 고치기

회원 검색과 로그인 조회만 있는 작은 Flask 앱에서 문자열로 이어 붙인 SQL이 어떻게 깨지는지 pytest와 쿼리 기록으로 확인합니다. ? 자리표시자, 정렬 기준 허용 목록, LIKE 와일드카드 이스케이프를 차례로 적용하고 Bandit B608이 사라지는 것까지 봅니다. 다만 스캐너가 조용하다는 것이 안전의 증거는 아니라는 점도 짚습니다.

글: https://copyandrun.com/blog/sql-parameter-binding-flask/

## 파일

- `app.py`
- `index.html`
- `queries.py`
- `queries_vulnerable.py`
- `requirements.txt`
- `test_queries.py`

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
