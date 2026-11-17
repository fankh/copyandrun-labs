# Ollama와 로컬 RAG로 PDF에 묻고 답하기

외부 서비스 없이 내 PC에서 PDF 문서에 질문하는 최소 RAG를 파이썬으로 만듭니다. pypdf 추출, 조각 나누기, Ollama 임베딩과 코사인 유사도 검색, 근거 표시, 근거 없는 질문 처리, 문서 속 지시문 실험까지 숫자로 확인합니다.

## 링크

- 글: [https://copyandrun.com/blog/local-rag-pdf-qa-ollama/](https://copyandrun.com/blog/local-rag-pdf-qa-ollama/)
- 한 번에 받기: [local-rag-pdf-qa-ollama.zip](https://copyandrun.com/code-zip/local-rag-pdf-qa-ollama.zip)
- GitHub 폴더: [copyandrun-labs/local-rag-pdf-qa-ollama](https://github.com/fankh/copyandrun-labs/tree/main/local-rag-pdf-qa-ollama)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `evaluate.py` | <a href="https://fankh.github.io/copyandrun-labs/local-rag-pdf-qa-ollama/evaluate.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/local-rag-pdf-qa-ollama/evaluate.py) |
| `extract_test.py` | <a href="https://fankh.github.io/copyandrun-labs/local-rag-pdf-qa-ollama/extract_test.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/local-rag-pdf-qa-ollama/extract_test.py) |
| `inject_test.py` | <a href="https://fankh.github.io/copyandrun-labs/local-rag-pdf-qa-ollama/inject_test.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/local-rag-pdf-qa-ollama/inject_test.py) |
| `make_pdf.py` | <a href="https://fankh.github.io/copyandrun-labs/local-rag-pdf-qa-ollama/make_pdf.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/local-rag-pdf-qa-ollama/make_pdf.py) |
| `rag.py` | <a href="https://fankh.github.io/copyandrun-labs/local-rag-pdf-qa-ollama/rag.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/local-rag-pdf-qa-ollama/rag.py) |
| `rag_web.py` | <a href="https://fankh.github.io/copyandrun-labs/local-rag-pdf-qa-ollama/rag_web.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/local-rag-pdf-qa-ollama/rag_web.py) |
| `repeat.py` | <a href="https://fankh.github.io/copyandrun-labs/local-rag-pdf-qa-ollama/repeat.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/local-rag-pdf-qa-ollama/repeat.py) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
