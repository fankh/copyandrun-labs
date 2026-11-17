# Sysmon 설치와 이벤트 1: 프로세스 해시와 부모 프로세스 기록, 4688 비교

Windows 11에 Microsoft Sysmon 15.22를 서명을 확인한 뒤 설치하고, 시험 활동만 기록하는 최소 설정으로 이벤트 1(프로세스 만들기)이 명령줄, 부모 프로세스, 해시를 남기는 것을 확인합니다. 감사 정책이 꺼져 4688이 남지 않는 PC에서 차이를 비교하고 깨끗이 제거합니다.

## 링크

- 글: [https://copyandrun.com/blog/windows-sysmon-install-process-create-event-1/](https://copyandrun.com/blog/windows-sysmon-install-process-create-event-1/)
- 한 번에 받기: [windows-sysmon-install-process-create-event-1.zip](https://copyandrun.com/code-zip/windows-sysmon-install-process-create-event-1.zip)
- GitHub 폴더: [copyandrun-labs/windows-sysmon-install-process-create-event-1](https://github.com/fankh/copyandrun-labs/tree/main/windows-sysmon-install-process-create-event-1)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `Get-SysmonEvents.ps1` | <a href="https://fankh.github.io/copyandrun-labs/windows-sysmon-install-process-create-event-1/Get-SysmonEvents.ps1" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/windows-sysmon-install-process-create-event-1/Get-SysmonEvents.ps1) |
| `sysmon-lab.xml` | <a href="https://fankh.github.io/copyandrun-labs/windows-sysmon-install-process-create-event-1/sysmon-lab.xml" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/windows-sysmon-install-process-create-event-1/sysmon-lab.xml) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
