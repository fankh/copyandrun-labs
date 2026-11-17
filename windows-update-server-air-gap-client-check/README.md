# 폐쇄망 Windows 업데이트 서버(WSUS) 구성과 클라이언트 점검

에어갭 망의 Windows 업데이트는 연결망 서버에서 업데이트 파일과 메타데이터를 내보내 폐쇄망 서버에 가져오는 방식입니다. 이 순서를 정리하고, 이 PC가 어디서 업데이트를 받는지와 인터넷으로 새어 나갈 길이 막혀 있는지 읽는 점검 스크립트를 직접 시험합니다.

## 링크

- 글: [https://copyandrun.com/blog/windows-update-server-air-gap-client-check/](https://copyandrun.com/blog/windows-update-server-air-gap-client-check/)
- 한 번에 받기: [windows-update-server-air-gap-client-check.zip](https://copyandrun.com/code-zip/windows-update-server-air-gap-client-check.zip)
- GitHub 폴더: [copyandrun-labs/windows-update-server-air-gap-client-check](https://github.com/fankh/copyandrun-labs/tree/main/windows-update-server-air-gap-client-check)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `Get-UpdateSourceConfig.ps1` | <a href="https://fankh.github.io/copyandrun-labs/windows-update-server-air-gap-client-check/Get-UpdateSourceConfig.ps1" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/windows-update-server-air-gap-client-check/Get-UpdateSourceConfig.ps1) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
