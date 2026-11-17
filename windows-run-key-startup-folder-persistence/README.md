# Windows Run 키와 시작 프로그램 폴더에 몰래 등록된 자동 실행 항목을 점검 스크립트로 찾기

Windows 11에서 로그온할 때 저절로 실행되는 Run 키와 시작 프로그램 폴더를 읽는 스크립트를 만들고, 무해한 시험 항목 두 개를 직접 등록해 찾아낸 뒤 지워서 처음 상태로 돌아온 것까지 확인합니다.

## 링크

- 글: [https://copyandrun.com/blog/windows-run-key-startup-folder-persistence/](https://copyandrun.com/blog/windows-run-key-startup-folder-persistence/)
- 한 번에 받기: [windows-run-key-startup-folder-persistence.zip](https://copyandrun.com/code-zip/windows-run-key-startup-folder-persistence.zip)
- GitHub 폴더: [copyandrun-labs/windows-run-key-startup-folder-persistence](https://github.com/fankh/copyandrun-labs/tree/main/windows-run-key-startup-folder-persistence)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `Get-AutoStartEntries.ps1` | <a href="https://fankh.github.io/copyandrun-labs/windows-run-key-startup-folder-persistence/Get-AutoStartEntries.ps1" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/windows-run-key-startup-folder-persistence/Get-AutoStartEntries.ps1) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
