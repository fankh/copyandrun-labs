# Windows 이벤트 4720, 4725, 4726, 4740 계정 기록 읽기

Windows 11에서 임시 로컬 계정을 만들고 비밀번호를 바꾸고 비활성화, 활성화, 잠금, 삭제하는 동안 남는 이벤트 4720, 4722, 4724, 4725, 4726, 4740을 PowerShell 스크립트로 한 줄씩 시간순으로 읽습니다.

## 링크

- 글: [https://copyandrun.com/blog/windows-event-4720-account-lifecycle-4740-lockout/](https://copyandrun.com/blog/windows-event-4720-account-lifecycle-4740-lockout/)
- 한 번에 받기: [windows-event-4720-account-lifecycle-4740-lockout.zip](https://copyandrun.com/code-zip/windows-event-4720-account-lifecycle-4740-lockout.zip)
- GitHub 폴더: [copyandrun-labs/windows-event-4720-account-lifecycle-4740-lockout](https://github.com/fankh/copyandrun-labs/tree/main/windows-event-4720-account-lifecycle-4740-lockout)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `Get-AccountChanges.ps1` | <a href="https://fankh.github.io/copyandrun-labs/windows-event-4720-account-lifecycle-4740-lockout/Get-AccountChanges.ps1" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/windows-event-4720-account-lifecycle-4740-lockout/Get-AccountChanges.ps1) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
