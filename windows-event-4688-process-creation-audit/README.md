# Windows 프로세스 만들기 감사와 명령줄 기록을 켜서 이벤트 4688로 실행 흔적 남기기

Hyper-V의 일회용 한국어 Windows 11 가상 머신에서 프로세스 만들기 감사가 꺼져 있어 실행 기록이 남지 않는 것을 확인하고, 로컬 그룹 정책 편집기로 감사와 명령줄 포함을 켠 뒤 whoami와 hostname 실행이 이벤트 4688로 남는 것을 이벤트 뷰어와 PowerShell로 대조합니다. 명령줄에 비밀번호가 그대로 남는 한계도 함께 확인합니다.

글: https://copyandrun.com/blog/windows-event-4688-process-creation-audit/

## 파일

- `Check-ProcessAudit.ps1`
- `process-view.xml`

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
