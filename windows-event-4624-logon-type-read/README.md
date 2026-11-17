# Windows 이벤트 4624 로그온 유형으로 로컬, 네트워크, 서비스 로그온을 구분해 읽기

Windows 11 보안 로그의 이벤트 4624를 PowerShell로 읽어 로그온 유형별로 세고, 서비스 로그온이 대부분인 로그에서 사람이 한 로그온만 골라내는 방법을 직접 만든 임시 계정의 로그온으로 확인합니다.

## 링크

- 글: [https://copyandrun.com/blog/windows-event-4624-logon-type-read/](https://copyandrun.com/blog/windows-event-4624-logon-type-read/)
- 한 번에 받기: [windows-event-4624-logon-type-read.zip](https://copyandrun.com/code-zip/windows-event-4624-logon-type-read.zip)
- GitHub 폴더: [copyandrun-labs/windows-event-4624-logon-type-read](https://github.com/fankh/copyandrun-labs/tree/main/windows-event-4624-logon-type-read)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `Get-LogonSummary.ps1` | <a href="https://fankh.github.io/copyandrun-labs/windows-event-4624-logon-type-read/Get-LogonSummary.ps1" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/windows-event-4624-logon-type-read/Get-LogonSummary.ps1) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
