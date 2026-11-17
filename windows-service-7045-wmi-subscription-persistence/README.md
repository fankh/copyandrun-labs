# Windows 새 서비스 등록 이벤트 7045와 WMI 이벤트 구독을 점검 스크립트로 찾고 지우기

Windows 11에서 시스템 권한으로 도는 서비스와 WMI 이벤트 구독은 재부팅 뒤에도 남는 은밀한 자동 실행 방법입니다. 무해한 시험 서비스와 구독을 직접 등록하고, 이벤트 7045와 5861과 점검 스크립트로 찾은 뒤 지워 처음 상태로 돌아온 것까지 확인합니다.

## 링크

- 글: [https://copyandrun.com/blog/windows-service-7045-wmi-subscription-persistence/](https://copyandrun.com/blog/windows-service-7045-wmi-subscription-persistence/)
- 한 번에 받기: [windows-service-7045-wmi-subscription-persistence.zip](https://copyandrun.com/code-zip/windows-service-7045-wmi-subscription-persistence.zip)
- GitHub 폴더: [copyandrun-labs/windows-service-7045-wmi-subscription-persistence](https://github.com/fankh/copyandrun-labs/tree/main/windows-service-7045-wmi-subscription-persistence)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `Get-ServiceAndWmiPersistence.ps1` | <a href="https://fankh.github.io/copyandrun-labs/windows-service-7045-wmi-subscription-persistence/Get-ServiceAndWmiPersistence.ps1" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/windows-service-7045-wmi-subscription-persistence/Get-ServiceAndWmiPersistence.ps1) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
