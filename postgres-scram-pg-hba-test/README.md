# PostgreSQL pg_hba.conf 점검: trust를 SCRAM과 접속 제한으로 바꾸기

pg_hba.conf가 trust로 열려 있는 PostgreSQL 16을 컨테이너로 띄우고, 다른 두 서버에서 같은 6가지 접속을 시도해 5칸이 어긋나는 것을 확인합니다. 규칙만 SCRAM으로 바꾸면 정상 앱까지 막히는 이유, 저장된 해시를 다시 만드는 순서, pg_hba_file_rules로 규칙을 교차 확인하는 방법과 종료 코드 게이트를 다룹니다.

글: https://copyandrun.com/blog/postgres-scram-pg-hba-test/

## 파일

- `hba_demo.sh`
- `pg_hba_bad.conf`
- `pg_hba_good.conf`

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
