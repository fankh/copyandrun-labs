# Ollama 임베딩으로 한국어 문장 유사도 재기: 잘 되는 곳과 약한 곳

nomic-embed-text로 한국어 문장 7개를 768차원 벡터로 바꾸고 코사인 유사도를 계산합니다. 같은 뜻의 문장은 잘 묶이지만 점수가 좁은 범위에 몰리고, 관련 없는 문장도 높게 나오는 약점까지 숫자로 확인합니다.

## 링크

- 글: [https://copyandrun.com/blog/ollama-embeddings-korean-similarity/](https://copyandrun.com/blog/ollama-embeddings-korean-similarity/)
- 한 번에 받기: [ollama-embeddings-korean-similarity.zip](https://copyandrun.com/code-zip/ollama-embeddings-korean-similarity.zip)
- GitHub 폴더: [copyandrun-labs/ollama-embeddings-korean-similarity](https://github.com/fankh/copyandrun-labs/tree/main/ollama-embeddings-korean-similarity)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `emb_more.py` | <a href="https://fankh.github.io/copyandrun-labs/ollama-embeddings-korean-similarity/emb_more.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/ollama-embeddings-korean-similarity/emb_more.py) |
| `embed_similarity.py` | <a href="https://fankh.github.io/copyandrun-labs/ollama-embeddings-korean-similarity/embed_similarity.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/ollama-embeddings-korean-similarity/embed_similarity.py) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
