# 생성형 AI가 짜 줄 법한 Flask 로그인 코드를 Semgrep으로 점검하기

프롬프트 세 가지(간단한 로그인, 비밀번호 저장 포함, 세션과 토큰 포함)에 AI가 내놓기 쉬운 형태로 직접 쓴 Flask 로그인 코드 세 벌을 Semgrep 레지스트리 규칙과 직접 쓴 규칙 세 개로 점검합니다. 변형별 결과 표, 수정 뒤 재점검, 도구가 잡지 못한 인증 논리 결함 두 가지를 직접 실행해 확인합니다.

## 링크

- 글: [https://copyandrun.com/blog/ai-generated-login-code-semgrep-review/](https://copyandrun.com/blog/ai-generated-login-code-semgrep-review/)
- 한 번에 받기: [ai-generated-login-code-semgrep-review.zip](https://copyandrun.com/code-zip/ai-generated-login-code-semgrep-review.zip)
- GitHub 폴더: [copyandrun-labs/ai-generated-login-code-semgrep-review](https://github.com/fankh/copyandrun-labs/tree/main/ai-generated-login-code-semgrep-review)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `Dockerfile` | <a href="https://fankh.github.io/copyandrun-labs/ai-generated-login-code-semgrep-review/Dockerfile" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/ai-generated-login-code-semgrep-review/Dockerfile) |
| `fixed_a.py` | <a href="https://fankh.github.io/copyandrun-labs/ai-generated-login-code-semgrep-review/fixed_a.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/ai-generated-login-code-semgrep-review/fixed_a.py) |
| `fixed_b.py` | <a href="https://fankh.github.io/copyandrun-labs/ai-generated-login-code-semgrep-review/fixed_b.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/ai-generated-login-code-semgrep-review/fixed_b.py) |
| `fixed_c.py` | <a href="https://fankh.github.io/copyandrun-labs/ai-generated-login-code-semgrep-review/fixed_c.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/ai-generated-login-code-semgrep-review/fixed_c.py) |
| `logic_check.py` | <a href="https://fankh.github.io/copyandrun-labs/ai-generated-login-code-semgrep-review/logic_check.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/ai-generated-login-code-semgrep-review/logic_check.py) |
| `login-extra.yml` | <a href="https://fankh.github.io/copyandrun-labs/ai-generated-login-code-semgrep-review/login-extra.yml" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/ai-generated-login-code-semgrep-review/login-extra.yml) |
| `login_a.py` | <a href="https://fankh.github.io/copyandrun-labs/ai-generated-login-code-semgrep-review/login_a.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/ai-generated-login-code-semgrep-review/login_a.py) |
| `login_b.py` | <a href="https://fankh.github.io/copyandrun-labs/ai-generated-login-code-semgrep-review/login_b.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/ai-generated-login-code-semgrep-review/login_b.py) |
| `login_c.py` | <a href="https://fankh.github.io/copyandrun-labs/ai-generated-login-code-semgrep-review/login_c.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/ai-generated-login-code-semgrep-review/login_c.py) |
| `scan.sh` | <a href="https://fankh.github.io/copyandrun-labs/ai-generated-login-code-semgrep-review/scan.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/ai-generated-login-code-semgrep-review/scan.sh) |
| `summarize.py` | <a href="https://fankh.github.io/copyandrun-labs/ai-generated-login-code-semgrep-review/summarize.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/ai-generated-login-code-semgrep-review/summarize.py) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
