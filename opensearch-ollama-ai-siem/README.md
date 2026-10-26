# Docker로 OpenSearch와 Ollama 띄워 비용 없는 AI-SIEM 만들기

OpenSearch와 로컬 LLM인 Ollama를 Docker로 띄우고, ml-commons 커넥터로 둘을 연결합니다. 로그에서 찾은 브루트포스 경보를 LLM이 세 줄로 분류하는 데까지 확인합니다.

글: https://copyandrun.com/blog/opensearch-ollama-ai-siem/

## 파일

- `classify.sh`
- `create_index_pattern.sh`
- `docker-compose.yml`
- `register_model.sh`
- `seed_logs.py`

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
