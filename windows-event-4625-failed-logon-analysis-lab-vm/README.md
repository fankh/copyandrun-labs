# Windows 이벤트 4625 로그온 실패를 분석하고 계정 잠금 정책으로 대응하기

Hyper-V의 일회용 Windows 11 가상 머신에서 로컬, 네트워크, 없는 계정의 로그온 실패를 직접 만들고, PowerShell 스크립트가 LOCAL ONLY와 REVIEW를 판정하는 과정을 이벤트 뷰어와 대조합니다. 잠금 임계값을 10회에서 5회로 낮춰 계정이 실제로 잠기는 것을 로컬 보안 정책 화면으로 확인합니다.

글: https://copyandrun.com/blog/windows-event-4625-failed-logon-analysis-lab-vm/

## 파일

- `Clean-LabFailures.ps1`
- `failed-logon-view.xml`
- `Get-FailedLogons.ps1`
- `New-LabFailures.ps1`

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
