# Windows 공유 폴더 접근 감사를 켜서 이벤트 5140과 5145로 누가 열었는지 남기기

공유 폴더를 만들고 접속해도 파일 공유 감사가 꺼져 있으면 기록이 남지 않는다는 것을 확인하고, 파일 공유 감사와 세부 파일 공유 감사를 켠 뒤 localhost로 접속한 기록이 이벤트 5140과 5145로 남는 것을 이벤트 뷰어와 점검 스크립트로 대조합니다. 5145가 많이 쌓이는 한계와 관리 공유를 따로 봐야 하는 이유도 함께 정리합니다.

## 링크

- 글: [https://copyandrun.com/blog/windows-smb-share-access-audit-5140/](https://copyandrun.com/blog/windows-smb-share-access-audit-5140/)
- 한 번에 받기: [windows-smb-share-access-audit-5140.zip](https://copyandrun.com/code-zip/windows-smb-share-access-audit-5140.zip)
- GitHub 폴더: [copyandrun-labs/windows-smb-share-access-audit-5140](https://github.com/fankh/copyandrun-labs/tree/main/windows-smb-share-access-audit-5140)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `Check-SmbShares.ps1` | <a href="https://fankh.github.io/copyandrun-labs/windows-smb-share-access-audit-5140/Check-SmbShares.ps1" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/windows-smb-share-access-audit-5140/Check-SmbShares.ps1) |
| `share-view.xml` | <a href="https://fankh.github.io/copyandrun-labs/windows-smb-share-access-audit-5140/share-view.xml" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/windows-smb-share-access-audit-5140/share-view.xml) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
