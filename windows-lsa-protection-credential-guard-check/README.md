# Windows LSA 보호와 Credential Guard(VBS) 켜짐 확인하기

Windows 11에서 레지스트리에 적힌 LSA 보호 설정과 실제로 동작 중인 상태를 따로 읽고, 부팅 때 남는 Wininit 이벤트 12, 14, 18로 보호된 프로세스로 시작되었는지 확인하는 점검 스크립트를 만듭니다.

## 링크

- 글: [https://copyandrun.com/blog/windows-lsa-protection-credential-guard-check/](https://copyandrun.com/blog/windows-lsa-protection-credential-guard-check/)
- 한 번에 받기: [windows-lsa-protection-credential-guard-check.zip](https://copyandrun.com/code-zip/windows-lsa-protection-credential-guard-check.zip)
- GitHub 폴더: [copyandrun-labs/windows-lsa-protection-credential-guard-check](https://github.com/fankh/copyandrun-labs/tree/main/windows-lsa-protection-credential-guard-check)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `Get-LsaProtection.ps1` | <a href="https://fankh.github.io/copyandrun-labs/windows-lsa-protection-credential-guard-check/Get-LsaProtection.ps1" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/windows-lsa-protection-credential-guard-check/Get-LsaProtection.ps1) |
| `Test-LsaConfigVsRunning.ps1` | <a href="https://fankh.github.io/copyandrun-labs/windows-lsa-protection-credential-guard-check/Test-LsaConfigVsRunning.ps1" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/windows-lsa-protection-credential-guard-check/Test-LsaConfigVsRunning.ps1) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
