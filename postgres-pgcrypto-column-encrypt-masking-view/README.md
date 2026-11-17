# pgcrypto로 컬럼 암호화하고 마스킹 뷰로 역할별 출력 나누기: 키가 서버 로그에 남는 문제까지

공식 postgres 이미지에서 pgcrypto의 pgp_sym_encrypt로 전화번호 컬럼을 암호화해 저장하고, 상담원 역할은 마스킹 뷰만, 관리자 역할은 복호화 뷰까지 읽게 GRANT를 나눕니다. 키를 SQL 문에 직접 쓰면 log_statement 로그와 pg_stat_statements에 남는 것을 확인하고, 바인드 매개변수와 로그 설정으로 줄이는 방법, 암호문 검색과 인덱스의 한계를 함께 봅니다.

## 링크

- 글: [https://copyandrun.com/blog/postgres-pgcrypto-column-encrypt-masking-view/](https://copyandrun.com/blog/postgres-pgcrypto-column-encrypt-masking-view/)
- 한 번에 받기: [postgres-pgcrypto-column-encrypt-masking-view.zip](https://copyandrun.com/code-zip/postgres-pgcrypto-column-encrypt-masking-view.zip)
- GitHub 폴더: [copyandrun-labs/postgres-pgcrypto-column-encrypt-masking-view](https://github.com/fankh/copyandrun-labs/tree/main/postgres-pgcrypto-column-encrypt-masking-view)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `admin_naive.sql` | <a href="https://fankh.github.io/copyandrun-labs/postgres-pgcrypto-column-encrypt-masking-view/admin_naive.sql" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/postgres-pgcrypto-column-encrypt-masking-view/admin_naive.sql) |
| `admin_safe.sql` | <a href="https://fankh.github.io/copyandrun-labs/postgres-pgcrypto-column-encrypt-masking-view/admin_safe.sql" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/postgres-pgcrypto-column-encrypt-masking-view/admin_safe.sql) |
| `agent_check.sql` | <a href="https://fankh.github.io/copyandrun-labs/postgres-pgcrypto-column-encrypt-masking-view/agent_check.sql" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/postgres-pgcrypto-column-encrypt-masking-view/agent_check.sql) |
| `log_params_off.sql` | <a href="https://fankh.github.io/copyandrun-labs/postgres-pgcrypto-column-encrypt-masking-view/log_params_off.sql" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/postgres-pgcrypto-column-encrypt-masking-view/log_params_off.sql) |
| `roles.sql` | <a href="https://fankh.github.io/copyandrun-labs/postgres-pgcrypto-column-encrypt-masking-view/roles.sql" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/postgres-pgcrypto-column-encrypt-masking-view/roles.sql) |
| `search_check.sql` | <a href="https://fankh.github.io/copyandrun-labs/postgres-pgcrypto-column-encrypt-masking-view/search_check.sql" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/postgres-pgcrypto-column-encrypt-masking-view/search_check.sql) |
| `seed.sql` | <a href="https://fankh.github.io/copyandrun-labs/postgres-pgcrypto-column-encrypt-masking-view/seed.sql" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/postgres-pgcrypto-column-encrypt-masking-view/seed.sql) |
| `setup.sql` | <a href="https://fankh.github.io/copyandrun-labs/postgres-pgcrypto-column-encrypt-masking-view/setup.sql" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/postgres-pgcrypto-column-encrypt-masking-view/setup.sql) |
| `start.sh` | <a href="https://fankh.github.io/copyandrun-labs/postgres-pgcrypto-column-encrypt-masking-view/start.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/postgres-pgcrypto-column-encrypt-masking-view/start.sh) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
