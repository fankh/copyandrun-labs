# Ollama 로컬 LLM에 입력 가드레일 붙이기

사용자 입력이 로컬 LLM에 닿기 전에 규칙 필터와 판정 모델 두 개를 거치게 하는 파이썬 스크립트를 만듭니다. 원문 대신 해시와 길이만 JSONL로 남기고, Ollama 장애 때 차단하는 방식을 확인하며, 철자 변형과 다른 언어로 우회되는 사례와 판정 모델의 오탐과 미탐을 실제 결과로 확인합니다.

## 링크

- 글: [https://copyandrun.com/blog/local-llm-input-guardrail/](https://copyandrun.com/blog/local-llm-input-guardrail/)
- 한 번에 받기: [local-llm-input-guardrail.zip](https://copyandrun.com/code-zip/local-llm-input-guardrail.zip)
- GitHub 폴더: [copyandrun-labs/local-llm-input-guardrail](https://github.com/fankh/copyandrun-labs/tree/main/local-llm-input-guardrail)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `guard.py` | <a href="https://fankh.github.io/copyandrun-labs/local-llm-input-guardrail/guard.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/local-llm-input-guardrail/guard.py) |
| `guard_web.py` | <a href="https://fankh.github.io/copyandrun-labs/local-llm-input-guardrail/guard_web.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/local-llm-input-guardrail/guard_web.py) |
| `limits.py` | <a href="https://fankh.github.io/copyandrun-labs/local-llm-input-guardrail/limits.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/local-llm-input-guardrail/limits.py) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
