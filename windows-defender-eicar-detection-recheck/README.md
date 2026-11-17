# Windows Defender EICAR 시험 파일 탐지 확인

Windows 11에서 실시간 보호를 끄고 EICAR 표준 시험 파일을 만들어 탐지되지 않는 것을 확인한 뒤, 실시간 보호를 켜고 같은 시험을 반복합니다. Windows 보안 앱의 보호 기록, 이벤트 뷰어의 이벤트 1116과 1117, PowerShell 점검 스크립트로 결과를 대조합니다.

## 링크

- 글: [https://copyandrun.com/blog/windows-defender-eicar-detection-recheck/](https://copyandrun.com/blog/windows-defender-eicar-detection-recheck/)
- 한 번에 받기: [windows-defender-eicar-detection-recheck.zip](https://copyandrun.com/code-zip/windows-defender-eicar-detection-recheck.zip)
- GitHub 폴더: [copyandrun-labs/windows-defender-eicar-detection-recheck](https://github.com/fankh/copyandrun-labs/tree/main/windows-defender-eicar-detection-recheck)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `Check-DefenderEicar.ps1` | <a href="https://fankh.github.io/copyandrun-labs/windows-defender-eicar-detection-recheck/Check-DefenderEicar.ps1" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/windows-defender-eicar-detection-recheck/Check-DefenderEicar.ps1) |
| `defender-view.xml` | <a href="https://fankh.github.io/copyandrun-labs/windows-defender-eicar-detection-recheck/defender-view.xml" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/windows-defender-eicar-detection-recheck/defender-view.xml) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
