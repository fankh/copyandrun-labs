# Windows 이벤트 4625 로그온 실패를 분석하고 계정 잠금 정책으로 대응하기

Windows 11에서 로컬, 네트워크, 없는 계정의 로그온 실패를 직접 만들고, PowerShell 스크립트가 LOCAL ONLY와 REVIEW를 판정하는 과정을 이벤트 뷰어와 대조합니다. 잠금 임계값을 10회에서 5회로 낮춰 계정이 실제로 잠기는 것을 로컬 보안 정책 화면으로 확인합니다.

## 링크

- 글: [https://copyandrun.com/blog/windows-event-4625-failed-logon-analysis/](https://copyandrun.com/blog/windows-event-4625-failed-logon-analysis/)
- 한 번에 받기: [windows-event-4625-failed-logon-analysis.zip](https://copyandrun.com/code-zip/windows-event-4625-failed-logon-analysis.zip)
- GitHub 폴더: [copyandrun-labs/windows-event-4625-failed-logon-analysis](https://github.com/fankh/copyandrun-labs/tree/main/windows-event-4625-failed-logon-analysis)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `failed-logon-view.xml` | <a href="https://fankh.github.io/copyandrun-labs/windows-event-4625-failed-logon-analysis/failed-logon-view.xml" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/windows-event-4625-failed-logon-analysis/failed-logon-view.xml) |
| `Get-FailedLogons.ps1` | <a href="https://fankh.github.io/copyandrun-labs/windows-event-4625-failed-logon-analysis/Get-FailedLogons.ps1" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/windows-event-4625-failed-logon-analysis/Get-FailedLogons.ps1) |
| `New-TestFailedLogons.ps1` | <a href="https://fankh.github.io/copyandrun-labs/windows-event-4625-failed-logon-analysis/New-TestFailedLogons.ps1" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/windows-event-4625-failed-logon-analysis/New-TestFailedLogons.ps1) |
| `Remove-TestFailedLogons.ps1` | <a href="https://fankh.github.io/copyandrun-labs/windows-event-4625-failed-logon-analysis/Remove-TestFailedLogons.ps1" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/windows-event-4625-failed-logon-analysis/Remove-TestFailedLogons.ps1) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
