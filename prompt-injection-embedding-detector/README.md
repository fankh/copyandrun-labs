# 임베딩 유사도로 프롬프트 인젝션 문장을 걸러 보기

Ollama 컨테이너의 nomic-embed-text 로 알려진 인젝션 문구와 입력 문장의 코사인 유사도를 구하는 파이썬 스크립트를 만듭니다. 임계값별 오탐과 미탐을 표로 확인하고, 이 방식이 인젝션의 절반 이상을 놓친다는 점과 긴 입력의 뒷부분이 잘리는 한계, 접두어와 규칙 필터를 바꿔 본 결과를 실제 수치로 봅니다.

글: https://copyandrun.com/blog/prompt-injection-embedding-detector/

## 파일

- `embed_guard.py`
- `embed_web.py`
- `eval.py`
- `truncate_check.py`

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
