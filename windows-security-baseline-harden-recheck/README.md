# Windows 보안 설정을 PowerShell로 점검하고 고친 뒤 다시 확인하기

Hyper-V의 일회용 Windows 11 가상 머신에서 방화벽, SMB, 원격 데스크톱 등 14개 항목을 읽기 전용 스크립트로 점검하고, 계획 미리보기를 거쳐 설정을 고친 뒤 재점검으로 PASS 7에서 PASS 12가 된 것을 Windows 보안 앱 화면과 함께 확인합니다.

글: https://copyandrun.com/blog/windows-security-baseline-harden-recheck/

## 파일

- `Check-WindowsSecurity.ps1`
- `Harden-WindowsSecurity.ps1`
- `Weaken-LabVm.ps1`

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
