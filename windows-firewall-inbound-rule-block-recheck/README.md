# Windows 방화벽 인바운드 차단 규칙: wf.msc로 만들고 이벤트 5152로 확인하기

수신 대기 중인 TCP 포트에 방화벽 규칙이 없다는 것을 확인하고, 고급 보안이 포함된 Windows Defender 방화벽에서 인바운드 차단 규칙을 만든 뒤, 같은 PC에서 자기 주소로 접속하는 확인이 규칙을 검증하지 못한다는 점과 필터링 플랫폼 이벤트 5152, 5156, 5157로 규칙의 적용을 확인하는 방법을 정리합니다.

## 링크

- 글: [https://copyandrun.com/blog/windows-firewall-inbound-rule-block-recheck/](https://copyandrun.com/blog/windows-firewall-inbound-rule-block-recheck/)
- 한 번에 받기: [windows-firewall-inbound-rule-block-recheck.zip](https://copyandrun.com/code-zip/windows-firewall-inbound-rule-block-recheck.zip)
- GitHub 폴더: [copyandrun-labs/windows-firewall-inbound-rule-block-recheck](https://github.com/fankh/copyandrun-labs/tree/main/windows-firewall-inbound-rule-block-recheck)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `Check-Firewall.ps1` | <a href="https://fankh.github.io/copyandrun-labs/windows-firewall-inbound-rule-block-recheck/Check-Firewall.ps1" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/windows-firewall-inbound-rule-block-recheck/Check-Firewall.ps1) |
| `firewall-view.xml` | <a href="https://fankh.github.io/copyandrun-labs/windows-firewall-inbound-rule-block-recheck/firewall-view.xml" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/windows-firewall-inbound-rule-block-recheck/firewall-view.xml) |
| `Reset-TestRules.ps1` | <a href="https://fankh.github.io/copyandrun-labs/windows-firewall-inbound-rule-block-recheck/Reset-TestRules.ps1" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/windows-firewall-inbound-rule-block-recheck/Reset-TestRules.ps1) |
| `Start-TestListener.ps1` | <a href="https://fankh.github.io/copyandrun-labs/windows-firewall-inbound-rule-block-recheck/Start-TestListener.ps1" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/windows-firewall-inbound-rule-block-recheck/Start-TestListener.ps1) |
| `Test-Port.ps1` | <a href="https://fankh.github.io/copyandrun-labs/windows-firewall-inbound-rule-block-recheck/Test-Port.ps1" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/windows-firewall-inbound-rule-block-recheck/Test-Port.ps1) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
