# Windows 작업 스케줄러에 몰래 생긴 작업을 이벤트 4698로 남기고 점검 스크립트로 찾기

작업 스케줄러에서 로그온 때 명령을 실행하는 작업을 만들어도 기록이 남지 않는다는 것을 확인하고, 기타 개체 액세스 이벤트 감사를 켜서 작업의 생성과 삭제가 이벤트 4698과 4699로 남는 것을 이벤트 뷰어로 대조합니다. Microsoft 폴더 밖의 작업을 나열하는 PowerShell 점검 스크립트와 그 한계도 함께 정리합니다.

## 링크

- 글: [https://copyandrun.com/blog/windows-scheduled-task-persistence-4698/](https://copyandrun.com/blog/windows-scheduled-task-persistence-4698/)
- 한 번에 받기: [windows-scheduled-task-persistence-4698.zip](https://copyandrun.com/code-zip/windows-scheduled-task-persistence-4698.zip)
- GitHub 폴더: [copyandrun-labs/windows-scheduled-task-persistence-4698](https://github.com/fankh/copyandrun-labs/tree/main/windows-scheduled-task-persistence-4698)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `Check-ScheduledTasks.ps1` | <a href="https://fankh.github.io/copyandrun-labs/windows-scheduled-task-persistence-4698/Check-ScheduledTasks.ps1" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/windows-scheduled-task-persistence-4698/Check-ScheduledTasks.ps1) |
| `task-view.xml` | <a href="https://fankh.github.io/copyandrun-labs/windows-scheduled-task-persistence-4698/task-view.xml" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/windows-scheduled-task-persistence-4698/task-view.xml) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
