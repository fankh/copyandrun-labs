# Sysmon 이벤트 3과 11로 PowerShell 내려받기 추적

Windows 11의 Sysmon에서 PowerShell이 로컬 웹 서버에서 파일을 내려받는 과정을 이벤트 1(프로세스), 3(네트워크 접속), 11(파일 생성)로 남기고, 같은 ProcessGuid로 묶어 누가 접속해 어떤 파일을 만들었는지 한 번에 읽는 방법을 정리합니다.

글: https://copyandrun.com/blog/windows-sysmon-network-file-create-events-3-11/

## 파일

- `Get-SysmonEvents.ps1`
- `sysmon-lab.xml`

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
