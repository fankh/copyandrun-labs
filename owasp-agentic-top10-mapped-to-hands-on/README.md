# OWASP 에이전트 앱 Top 10을 내가 해 본 실습 결과에 대응시키기

OWASP Top 10 for Agentic Applications 2026의 ASI01부터 ASI10까지를 이 블로그에서 직접 실행해 본 글과 하나씩 맞춰 봅니다. 확인한 관찰은 링크로 잇고, 시험하지 않은 항목은 그렇다고 표시한 뒤 점검 체크리스트만 남깁니다. 대응 표, 화면 앱, 링크 점검 스크립트를 함께 싣습니다.

## 링크

- 글: [https://copyandrun.com/blog/owasp-agentic-top10-mapped-to-hands-on/](https://copyandrun.com/blog/owasp-agentic-top10-mapped-to-hands-on/)
- 한 번에 받기: [owasp-agentic-top10-mapped-to-hands-on.zip](https://copyandrun.com/code-zip/owasp-agentic-top10-mapped-to-hands-on.zip)
- GitHub 폴더: [copyandrun-labs/owasp-agentic-top10-mapped-to-hands-on](https://github.com/fankh/copyandrun-labs/tree/main/owasp-agentic-top10-mapped-to-hands-on)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `asi_mapping.json` | <a href="https://fankh.github.io/copyandrun-labs/owasp-agentic-top10-mapped-to-hands-on/asi_mapping.json" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/owasp-agentic-top10-mapped-to-hands-on/asi_mapping.json) |
| `asi_table.py` | <a href="https://fankh.github.io/copyandrun-labs/owasp-agentic-top10-mapped-to-hands-on/asi_table.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/owasp-agentic-top10-mapped-to-hands-on/asi_table.py) |
| `check_asi_mapping.py` | <a href="https://fankh.github.io/copyandrun-labs/owasp-agentic-top10-mapped-to-hands-on/check_asi_mapping.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/owasp-agentic-top10-mapped-to-hands-on/check_asi_mapping.py) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
