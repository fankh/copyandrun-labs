# Linux 계정 점검: UID 0 계정, 빈 암호, 로그인 셸이 있는 시스템 계정을 awk로 찾기

/etc/passwd와 /etc/shadow에서 root 말고 UID 0인 계정, 빈 암호 계정, 중복 UID, 로그인 셸을 가진 시스템 계정을 찾는 읽기 전용 스크립트를 만듭니다. 실제 Ubuntu에서 실행하면 sync 계정이 걸리는 이유와 시험 파일에서 5건이 0건이 되는 과정을 화면으로 확인합니다.

글: https://copyandrun.com/blog/account-audit-uid0-empty-password/

## 파일

- `account-audit.sh`

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
