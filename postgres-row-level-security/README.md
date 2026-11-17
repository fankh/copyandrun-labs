# PostgreSQL 행 수준 보안(RLS) 실습: 기본 거부, FORCE

한 표를 여러 사용자가 나눠 쓸 때 남의 행을 읽고 고치지 못하게 하는 RLS를 PostgreSQL 16 컨테이너에서 단계별로 확인합니다. 정책이 없을 때 모두 보이는 문제, 켜기만 하면 0행이 되는 기본 거부, 표 소유자와 슈퍼유저의 우회, FORCE로 소유자까지 묶는 방법을 같은 질의로 비교하고 합격 판정을 종료 코드로 냅니다.

## 링크

- 글: [https://copyandrun.com/blog/postgres-row-level-security/](https://copyandrun.com/blog/postgres-row-level-security/)
- 한 번에 받기: [postgres-row-level-security.zip](https://copyandrun.com/code-zip/postgres-row-level-security.zip)
- GitHub 폴더: [copyandrun-labs/postgres-row-level-security](https://github.com/fankh/copyandrun-labs/tree/main/postgres-row-level-security)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `rls_demo.sh` | <a href="https://fankh.github.io/copyandrun-labs/postgres-row-level-security/rls_demo.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/postgres-row-level-security/rls_demo.sh) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
