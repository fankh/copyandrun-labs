# Windows 로컬 Administrators 그룹에 계정이 추가된 변경을 이벤트 4720과 4732로 남기고 조회하기

Hyper-V의 일회용 한국어 Windows 11 가상 머신에서 계정 관리 감사를 끈 채 테스트 계정을 만들고 Administrators 그룹에 넣으면 기록이 하나도 남지 않는 것을 확인합니다. 로컬 그룹 정책 편집기로 사용자 계정 관리와 보안 그룹 관리 감사를 켠 뒤 같은 변경을 다시 해서 이벤트 4720과 4732를 이벤트 뷰어와 PowerShell 조회 스크립트로 확인하고, 테스트 계정을 지웁니다.

글: https://copyandrun.com/blog/windows-event-4732-local-admin-group-change/

## 파일

- `account-view.xml`
- `Get-AccountChanges.ps1`

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
