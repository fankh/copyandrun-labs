# Flask에서 SQL 쿼리를 파라미터 바인딩으로 고치기

회원 검색과 로그인 조회만 있는 작은 Flask 앱에서 문자열로 이어 붙인 SQL이 어떻게 깨지는지 pytest와 쿼리 기록으로 확인합니다. ? 자리표시자, 정렬 기준 허용 목록, LIKE 와일드카드 이스케이프를 차례로 적용하고 Bandit B608이 사라지는 것까지 봅니다. 다만 스캐너가 조용하다는 것이 안전의 증거는 아니라는 점도 짚습니다.

## 링크

- 글: [https://copyandrun.com/blog/sql-parameter-binding-flask/](https://copyandrun.com/blog/sql-parameter-binding-flask/)
- 한 번에 받기: [sql-parameter-binding-flask.zip](https://copyandrun.com/code-zip/sql-parameter-binding-flask.zip)
- GitHub 폴더: [copyandrun-labs/sql-parameter-binding-flask](https://github.com/fankh/copyandrun-labs/tree/main/sql-parameter-binding-flask)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `app.py` | <a href="https://fankh.github.io/copyandrun-labs/sql-parameter-binding-flask/app.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/sql-parameter-binding-flask/app.py) |
| `index.html` | <a href="https://fankh.github.io/copyandrun-labs/sql-parameter-binding-flask/index.html" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/sql-parameter-binding-flask/index.html) |
| `queries.py` | <a href="https://fankh.github.io/copyandrun-labs/sql-parameter-binding-flask/queries.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/sql-parameter-binding-flask/queries.py) |
| `queries_vulnerable.py` | <a href="https://fankh.github.io/copyandrun-labs/sql-parameter-binding-flask/queries_vulnerable.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/sql-parameter-binding-flask/queries_vulnerable.py) |
| `requirements.txt` | <a href="https://fankh.github.io/copyandrun-labs/sql-parameter-binding-flask/requirements.txt" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/sql-parameter-binding-flask/requirements.txt) |
| `test_queries.py` | <a href="https://fankh.github.io/copyandrun-labs/sql-parameter-binding-flask/test_queries.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/sql-parameter-binding-flask/test_queries.py) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
