# Windows 보안 설정을 PowerShell로 점검하고 고친 뒤 다시 확인하기

Windows 11에서 방화벽, SMB, 원격 데스크톱 등 14개 항목을 읽기 전용 스크립트로 점검하고, 계획 미리보기를 거쳐 설정을 고친 뒤 재점검으로 PASS 7에서 PASS 12가 된 것을 Windows 보안 앱 화면과 함께 확인합니다.

## 링크

- 글: [https://copyandrun.com/blog/windows-security-baseline-harden-recheck/](https://copyandrun.com/blog/windows-security-baseline-harden-recheck/)
- 한 번에 받기: [windows-security-baseline-harden-recheck.zip](https://copyandrun.com/code-zip/windows-security-baseline-harden-recheck.zip)
- GitHub 폴더: [copyandrun-labs/windows-security-baseline-harden-recheck](https://github.com/fankh/copyandrun-labs/tree/main/windows-security-baseline-harden-recheck)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `Check-WindowsSecurity.ps1` | <a href="https://fankh.github.io/copyandrun-labs/windows-security-baseline-harden-recheck/Check-WindowsSecurity.ps1" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/windows-security-baseline-harden-recheck/Check-WindowsSecurity.ps1) |
| `Harden-WindowsSecurity.ps1` | <a href="https://fankh.github.io/copyandrun-labs/windows-security-baseline-harden-recheck/Harden-WindowsSecurity.ps1" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/windows-security-baseline-harden-recheck/Harden-WindowsSecurity.ps1) |
| `Set-InsecureBaseline.ps1` | <a href="https://fankh.github.io/copyandrun-labs/windows-security-baseline-harden-recheck/Set-InsecureBaseline.ps1" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/windows-security-baseline-harden-recheck/Set-InsecureBaseline.ps1) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
