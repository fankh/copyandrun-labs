# MySQL 8.0 사용자와 권한 감사: 빈 비밀번호, 와일드카드

MySQL 8.0 컨테이너에 일부러 느슨한 계정을 만들고, mysql.user와 information_schema 질의로 빈 비밀번호, % 호스트, GRANT OPTION 전역 권한을 찾는 감사 스크립트를 돌립니다. HIGH 발견 4건을 최소 권한으로 고쳐 0건으로 만들고, 실제 접속 시험 8칸과 SHOW GRANTS로 교차 확인한 뒤 종료 코드로 판정합니다.

글: https://copyandrun.com/blog/mysql-user-grants-audit/

## 파일

- `mysql_audit_demo.sh`

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
