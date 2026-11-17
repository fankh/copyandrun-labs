# Sysmon 프로세스 생성 로그로 부모 자식 트리 그리기: 문서 앱이 셸을 띄우는 모양 찾기

공개 Sysmon EVTX 샘플에서 이벤트 ID 1(프로세스 생성)을 읽어 ProcessGuid와 ParentProcessGuid로 프로세스 트리를 그리고, Office 계열 프로세스가 cmd나 rundll32 같은 실행 파일을 자식으로 둔 경우를 표시하는 파이썬 스크립트를 만들어 돌립니다. 탐지 규칙 아이디어와 오탐 사례도 정리합니다.

## 링크

- 글: [https://copyandrun.com/blog/sysmon-process-tree-office-powershell/](https://copyandrun.com/blog/sysmon-process-tree-office-powershell/)
- 한 번에 받기: [sysmon-process-tree-office-powershell.zip](https://copyandrun.com/code-zip/sysmon-process-tree-office-powershell.zip)
- GitHub 폴더: [copyandrun-labs/sysmon-process-tree-office-powershell](https://github.com/fankh/copyandrun-labs/tree/main/sysmon-process-tree-office-powershell)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `Dockerfile` | <a href="https://fankh.github.io/copyandrun-labs/sysmon-process-tree-office-powershell/Dockerfile" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/sysmon-process-tree-office-powershell/Dockerfile) |
| `evtx_tree.py` | <a href="https://fankh.github.io/copyandrun-labs/sysmon-process-tree-office-powershell/evtx_tree.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/sysmon-process-tree-office-powershell/evtx_tree.py) |
| `fetch.sh` | <a href="https://fankh.github.io/copyandrun-labs/sysmon-process-tree-office-powershell/fetch.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/sysmon-process-tree-office-powershell/fetch.sh) |
| `test_rules.py` | <a href="https://fankh.github.io/copyandrun-labs/sysmon-process-tree-office-powershell/test_rules.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/sysmon-process-tree-office-powershell/test_rules.py) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
