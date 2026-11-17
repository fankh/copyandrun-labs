# PostgreSQL 역할 최소 권한 실습: PUBLIC 회수, 기본 권한

앱 역할이 표 주인이고 읽기 역할에 ALL이 주어진 느슨한 PostgreSQL을 최소 권한으로 고칩니다. 같은 12칸짜리 허용/거부 표로 전후를 검사해 어긋난 칸이 6개에서 0개가 되는 것을 확인하고, 나중에 만든 표에 권한이 자동으로 붙는 기본 권한(DEFAULT PRIVILEGES)과 has_table_privilege 교차 확인까지 다룹니다.

글: https://copyandrun.com/blog/postgres-roles-least-privilege/

## 파일

- `roles_demo.sh`

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
