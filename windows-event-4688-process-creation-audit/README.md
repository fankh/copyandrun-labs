# Windows 프로세스 만들기 감사와 명령줄 기록을 켜서 이벤트 4688로 실행 흔적 남기기

Windows 11에서 프로세스 만들기 감사가 꺼져 있어 실행 기록이 남지 않는 것을 확인하고, 로컬 그룹 정책 편집기로 감사와 명령줄 포함을 켠 뒤 whoami와 hostname 실행이 이벤트 4688로 남는 것을 이벤트 뷰어와 PowerShell로 대조합니다. 명령줄에 비밀번호가 그대로 남는 한계도 함께 확인합니다.

## 링크

- 글: [https://copyandrun.com/blog/windows-event-4688-process-creation-audit/](https://copyandrun.com/blog/windows-event-4688-process-creation-audit/)
- 한 번에 받기: [windows-event-4688-process-creation-audit.zip](https://copyandrun.com/code-zip/windows-event-4688-process-creation-audit.zip)
- GitHub 폴더: [copyandrun-labs/windows-event-4688-process-creation-audit](https://github.com/fankh/copyandrun-labs/tree/main/windows-event-4688-process-creation-audit)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `Check-ProcessAudit.ps1` | <a href="https://fankh.github.io/copyandrun-labs/windows-event-4688-process-creation-audit/Check-ProcessAudit.ps1" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/windows-event-4688-process-creation-audit/Check-ProcessAudit.ps1) |
| `process-view.xml` | <a href="https://fankh.github.io/copyandrun-labs/windows-event-4688-process-creation-audit/process-view.xml" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/windows-event-4688-process-creation-audit/process-view.xml) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
