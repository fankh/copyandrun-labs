# OpenLDAP ACL 점검하기: 익명과 로그인 사용자가 비밀번호 해시를 읽을 수 있는지 확인

OpenLDAP 2.6.15 컨테이너 두 개에 같은 사용자 항목을 넣고, 느슨한 ACL과 좁힌 ACL을 익명과 일반 사용자로 나누어 검색과 수정을 시도합니다. slapacl로 같은 질문을 설정 파일만으로 대조하고, 막혀야 하는 동작이 허용되는 건수를 종료 코드로 바꿉니다.

글: https://copyandrun.com/blog/openldap-acl-anonymous-vs-bound/

## 파일

- `ldap_demo.sh`
- `slapd_bad.conf`
- `slapd_good.conf`
- `users.ldif`

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
