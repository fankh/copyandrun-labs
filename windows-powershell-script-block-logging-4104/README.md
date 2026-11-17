# PowerShell 스크립트 블록 로깅을 켜서 이벤트 4104로 실행한 스크립트 내용 남기기

스크립트 블록 로깅이 꺼져 있으면 PowerShell에서 실행한 명령의 내용이 남지 않는다는 것을 확인하고, 로컬 그룹 정책 편집기에서 PowerShell 스크립트 블록 로깅을 켠 뒤 Get-Date와 whoami 실행이 이벤트 4104로 남는 것을 이벤트 뷰어와 점검 스크립트로 대조합니다. 비밀값이 로그에 그대로 남는 한계와 난독화된 명령의 기록 방식도 함께 확인합니다.

## 링크

- 글: [https://copyandrun.com/blog/windows-powershell-script-block-logging-4104/](https://copyandrun.com/blog/windows-powershell-script-block-logging-4104/)
- 한 번에 받기: [windows-powershell-script-block-logging-4104.zip](https://copyandrun.com/code-zip/windows-powershell-script-block-logging-4104.zip)
- GitHub 폴더: [copyandrun-labs/windows-powershell-script-block-logging-4104](https://github.com/fankh/copyandrun-labs/tree/main/windows-powershell-script-block-logging-4104)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `Check-ScriptBlockLogging.ps1` | <a href="https://fankh.github.io/copyandrun-labs/windows-powershell-script-block-logging-4104/Check-ScriptBlockLogging.ps1" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/windows-powershell-script-block-logging-4104/Check-ScriptBlockLogging.ps1) |
| `script-block-view.xml` | <a href="https://fankh.github.io/copyandrun-labs/windows-powershell-script-block-logging-4104/script-block-view.xml" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/windows-powershell-script-block-logging-4104/script-block-view.xml) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
