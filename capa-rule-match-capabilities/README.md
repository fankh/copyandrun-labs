# capa로 실행 파일의 기능 규칙 맞춰 보기: 어떤 동작을 근거로 판단하는지

Mandiant의 capa로 직접 컴파일한 시험 프로그램 세 개를 실행하지 않고 분석합니다. 규칙 이름, ATT&CK와 MBC 항목, 함수 주소와 API 근거를 읽고, JSON 결과를 파이썬으로 표로 요약합니다. capa가 기능의 존재를 알려 줄 뿐 악성 여부는 판정하지 않는다는 점도 결과로 확인합니다.

## 링크

- 글: [https://copyandrun.com/blog/capa-rule-match-capabilities/](https://copyandrun.com/blog/capa-rule-match-capabilities/)
- 한 번에 받기: [capa-rule-match-capabilities.zip](https://copyandrun.com/code-zip/capa-rule-match-capabilities.zip)
- GitHub 폴더: [copyandrun-labs/capa-rule-match-capabilities](https://github.com/fankh/copyandrun-labs/tree/main/capa-rule-match-capabilities)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `build.sh` | <a href="https://fankh.github.io/copyandrun-labs/capa-rule-match-capabilities/build.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/capa-rule-match-capabilities/build.sh) |
| `empty.c` | <a href="https://fankh.github.io/copyandrun-labs/capa-rule-match-capabilities/empty.c" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/capa-rule-match-capabilities/empty.c) |
| `fileio.c` | <a href="https://fankh.github.io/copyandrun-labs/capa-rule-match-capabilities/fileio.c" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/capa-rule-match-capabilities/fileio.c) |
| `run_capa.sh` | <a href="https://fankh.github.io/copyandrun-labs/capa-rule-match-capabilities/run_capa.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/capa-rule-match-capabilities/run_capa.sh) |
| `setup.sh` | <a href="https://fankh.github.io/copyandrun-labs/capa-rule-match-capabilities/setup.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/capa-rule-match-capabilities/setup.sh) |
| `sockdemo.c` | <a href="https://fankh.github.io/copyandrun-labs/capa-rule-match-capabilities/sockdemo.c" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/capa-rule-match-capabilities/sockdemo.c) |
| `summarize.py` | <a href="https://fankh.github.io/copyandrun-labs/capa-rule-match-capabilities/summarize.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/capa-rule-match-capabilities/summarize.py) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
