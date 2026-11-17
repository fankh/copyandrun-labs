# Windows 이벤트 4672 특별 권한 로그온으로 관리자급 로그온을 찾고 일반 사용자와 비교하기

Windows 11에서 일반 사용자와 Administrators 그룹 사용자가 로그온할 때 이벤트 4672가 어떻게 달라지는지 임시 계정으로 확인하고, PowerShell 스크립트가 4624와 짝을 지어 로그온 유형과 강한 권한을 보여 주는 과정을 따라 합니다.

## 링크

- 글: [https://copyandrun.com/blog/windows-event-4672-special-privileges-logon/](https://copyandrun.com/blog/windows-event-4672-special-privileges-logon/)
- 한 번에 받기: [windows-event-4672-special-privileges-logon.zip](https://copyandrun.com/code-zip/windows-event-4672-special-privileges-logon.zip)
- GitHub 폴더: [copyandrun-labs/windows-event-4672-special-privileges-logon](https://github.com/fankh/copyandrun-labs/tree/main/windows-event-4672-special-privileges-logon)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `Get-PrivilegedLogons.ps1` | <a href="https://fankh.github.io/copyandrun-labs/windows-event-4672-special-privileges-logon/Get-PrivilegedLogons.ps1" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/windows-event-4672-special-privileges-logon/Get-PrivilegedLogons.ps1) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
