# Ollama와 로컬 RAG로 PDF에 묻고 답하기

외부 서비스 없이 내 PC에서 PDF 문서에 질문하는 최소 RAG를 파이썬으로 만듭니다. pypdf 추출, 조각 나누기, Ollama 임베딩과 코사인 유사도 검색, 근거 표시, 근거 없는 질문 처리, 문서 속 지시문 실험까지 숫자로 확인합니다.

글: https://copyandrun.com/blog/local-rag-pdf-qa-ollama/

## 파일

- `evaluate.py`
- `extract_test.py`
- `inject_test.py`
- `make_pdf.py`
- `rag.py`
- `rag_web.py`
- `repeat.py`

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
