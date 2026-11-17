# Ollama 임베딩으로 한국어 문장 유사도 재기: 잘 되는 곳과 약한 곳

nomic-embed-text로 한국어 문장 7개를 768차원 벡터로 바꾸고 코사인 유사도를 계산합니다. 같은 뜻의 문장은 잘 묶이지만 점수가 좁은 범위에 몰리고, 관련 없는 문장도 높게 나오는 약점까지 숫자로 확인합니다.

글: https://copyandrun.com/blog/ollama-embeddings-korean-similarity/

## 파일

- `emb_more.py`
- `embed_similarity.py`

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
