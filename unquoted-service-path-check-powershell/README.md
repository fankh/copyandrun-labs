# Windows 서비스 경로 따옴표 누락 점검: PowerShell로 찾기

Windows 서비스의 실행 파일 경로에 공백이 있는데 따옴표가 없으면 권한 상승 경로가 될 수 있습니다. 서비스 경로를 읽기만 해서 이런 서비스를 세는 PowerShell 스크립트를 만들고, 판정 함수를 시험 경로 네 개로 확인합니다.

## 링크

- 글: [https://copyandrun.com/blog/unquoted-service-path-check-powershell/](https://copyandrun.com/blog/unquoted-service-path-check-powershell/)
- 한 번에 받기: [unquoted-service-path-check-powershell.zip](https://copyandrun.com/code-zip/unquoted-service-path-check-powershell.zip)
- GitHub 폴더: [copyandrun-labs/unquoted-service-path-check-powershell](https://github.com/fankh/copyandrun-labs/tree/main/unquoted-service-path-check-powershell)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `Check-UnquotedServicePath.ps1` | <a href="https://fankh.github.io/copyandrun-labs/unquoted-service-path-check-powershell/Check-UnquotedServicePath.ps1" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/unquoted-service-path-check-powershell/Check-UnquotedServicePath.ps1) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
