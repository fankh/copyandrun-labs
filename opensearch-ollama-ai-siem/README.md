# Docker로 OpenSearch와 Ollama 띄워 비용 없는 AI-SIEM 만들기

OpenSearch와 로컬 LLM인 Ollama를 Docker로 띄우고, ml-commons 커넥터로 둘을 연결합니다. 로그에서 찾은 브루트포스 경보를 LLM이 세 줄로 분류하는 데까지 확인합니다.

## 링크

- 글: [https://copyandrun.com/blog/opensearch-ollama-ai-siem/](https://copyandrun.com/blog/opensearch-ollama-ai-siem/)
- 한 번에 받기: [opensearch-ollama-ai-siem.zip](https://copyandrun.com/code-zip/opensearch-ollama-ai-siem.zip)
- GitHub 폴더: [copyandrun-labs/opensearch-ollama-ai-siem](https://github.com/fankh/copyandrun-labs/tree/main/opensearch-ollama-ai-siem)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `classify.sh` | <a href="https://fankh.github.io/copyandrun-labs/opensearch-ollama-ai-siem/classify.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/opensearch-ollama-ai-siem/classify.sh) |
| `create_index_pattern.sh` | <a href="https://fankh.github.io/copyandrun-labs/opensearch-ollama-ai-siem/create_index_pattern.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/opensearch-ollama-ai-siem/create_index_pattern.sh) |
| `docker-compose.yml` | <a href="https://fankh.github.io/copyandrun-labs/opensearch-ollama-ai-siem/docker-compose.yml" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/opensearch-ollama-ai-siem/docker-compose.yml) |
| `register_model.sh` | <a href="https://fankh.github.io/copyandrun-labs/opensearch-ollama-ai-siem/register_model.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/opensearch-ollama-ai-siem/register_model.sh) |
| `seed_logs.py` | <a href="https://fankh.github.io/copyandrun-labs/opensearch-ollama-ai-siem/seed_logs.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/opensearch-ollama-ai-siem/seed_logs.py) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
