# 작은 모델의 출력 형식을 고정하기: llama-server의 JSON 스키마와 GBNF 문법

프롬프트로 JSON을 부탁하면 1B 모델은 열두 번 중 열 번만 읽히고 한 번도 스키마에 맞지 않았습니다. llama-server의 json_schema와 GBNF 문법으로 출력을 제한하면 어떻게 달라지는지, 형식은 지켜져도 내용의 정확도는 그대로인 점까지 모델 두 개로 비교합니다.

## 링크

- 글: [https://copyandrun.com/blog/llama-server-json-schema-grammar/](https://copyandrun.com/blog/llama-server-json-schema-grammar/)
- 한 번에 받기: [llama-server-json-schema-grammar.zip](https://copyandrun.com/code-zip/llama-server-json-schema-grammar.zip)
- GitHub 폴더: [copyandrun-labs/llama-server-json-schema-grammar](https://github.com/fankh/copyandrun-labs/tree/main/llama-server-json-schema-grammar)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `constrained_demo.py` | <a href="https://fankh.github.io/copyandrun-labs/llama-server-json-schema-grammar/constrained_demo.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/llama-server-json-schema-grammar/constrained_demo.py) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
