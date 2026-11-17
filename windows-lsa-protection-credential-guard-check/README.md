# Windows LSA 보호와 Credential Guard(VBS) 켜짐 확인하기

Windows 11에서 레지스트리에 적힌 LSA 보호 설정과 실제로 동작 중인 상태를 따로 읽고, 부팅 때 남는 Wininit 이벤트 12, 14, 18로 보호된 프로세스로 시작되었는지 확인하는 점검 스크립트를 만듭니다.

글: https://copyandrun.com/blog/windows-lsa-protection-credential-guard-check/

## 파일

- `Get-LsaProtection.ps1`
- `Test-LsaConfigVsRunning.ps1`

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
