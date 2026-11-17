# Java JDBC SQL 인젝션 막기: PreparedStatement 비교

H2 인메모리 DB와 Java 21로 로그인과 검색 코드를 문자열 이어붙이기로 만들어 학습용 입력으로 의도치 않은 행이 반환되는 것을 확인하고, PreparedStatement로 고쳐 같은 입력이 막히는 것을 표로 비교합니다. ORDER BY 자리는 허용 목록으로, LIKE의 와일드카드는 이스케이프로 처리하고, 읽기 전용 DB 계정이 쓰기를 거부하는 것까지 실행해 확인합니다.

## 링크

- 글: [https://copyandrun.com/blog/java-jdbc-preparedstatement-sqli/](https://copyandrun.com/blog/java-jdbc-preparedstatement-sqli/)
- 한 번에 받기: [java-jdbc-preparedstatement-sqli.zip](https://copyandrun.com/code-zip/java-jdbc-preparedstatement-sqli.zip)
- GitHub 폴더: [copyandrun-labs/java-jdbc-preparedstatement-sqli](https://github.com/fankh/copyandrun-labs/tree/main/java-jdbc-preparedstatement-sqli)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `App.java` | <a href="https://fankh.github.io/copyandrun-labs/java-jdbc-preparedstatement-sqli/App.java" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/java-jdbc-preparedstatement-sqli/App.java) |
| `Db.java` | <a href="https://fankh.github.io/copyandrun-labs/java-jdbc-preparedstatement-sqli/Db.java" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/java-jdbc-preparedstatement-sqli/Db.java) |
| `Dockerfile` | <a href="https://fankh.github.io/copyandrun-labs/java-jdbc-preparedstatement-sqli/Dockerfile" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/java-jdbc-preparedstatement-sqli/Dockerfile) |
| `Fixed.java` | <a href="https://fankh.github.io/copyandrun-labs/java-jdbc-preparedstatement-sqli/Fixed.java" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/java-jdbc-preparedstatement-sqli/Fixed.java) |
| `Vulnerable.java` | <a href="https://fankh.github.io/copyandrun-labs/java-jdbc-preparedstatement-sqli/Vulnerable.java" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/java-jdbc-preparedstatement-sqli/Vulnerable.java) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
