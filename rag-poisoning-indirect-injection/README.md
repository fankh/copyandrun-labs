# RAG 포이즈닝과 간접 프롬프트 인젝션을 로컬에서 재현하기

문서 한 건이 RAG 챗봇의 컨텍스트에 섞여 들어가는 과정과 권한 밖 문서가 검색되는 과정을 로컬에서 재현합니다. 접근 제어와 지시문 필터를 걸어 막아 보고, 필터가 우회되는 지점까지 확인합니다.

## 링크

- 글: [https://copyandrun.com/blog/rag-poisoning-indirect-injection/](https://copyandrun.com/blog/rag-poisoning-indirect-injection/)
- 한 번에 받기: [rag-poisoning-indirect-injection.zip](https://copyandrun.com/code-zip/rag-poisoning-indirect-injection.zip)
- GitHub 폴더: [copyandrun-labs/rag-poisoning-indirect-injection](https://github.com/fankh/copyandrun-labs/tree/main/rag-poisoning-indirect-injection)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `rag_lab.py` | <a href="https://fankh.github.io/copyandrun-labs/rag-poisoning-indirect-injection/rag_lab.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/rag-poisoning-indirect-injection/rag_lab.py) |
| `rag_web.py` | <a href="https://fankh.github.io/copyandrun-labs/rag-poisoning-indirect-injection/rag_web.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/rag-poisoning-indirect-injection/rag_web.py) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
