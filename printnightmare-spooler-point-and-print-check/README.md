# PrintNightmare 점검: Print Spooler와 Point and Print 정책 확인

PrintNightmare(CVE-2021-34527)는 업데이트 외에 Point and Print 레지스트리 값 두 개가 0이거나 정의되지 않아야 안전합니다. Print Spooler 서비스 상태와 이 값을 읽기 전용으로 확인하는 PowerShell 스크립트를 만들고, 판정 함수를 시험 값으로 확인합니다.

글: https://copyandrun.com/blog/printnightmare-spooler-point-and-print-check/

## 파일

- `Check-PrintNightmare.ps1`

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
