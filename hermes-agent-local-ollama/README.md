# 로컬 Ollama 모델을 Hermes Agent에 연결하기

호스트의 Ollama 모델을 hermes model의 사용자 지정 엔드포인트로 연결하고, 컨텍스트가 32K인 작은 모델이 왜 실패하는지 로그로 확인한 뒤, 64K 컨텍스트 Modelfile로 만든 27B 모델에서 도구 호출까지 되는 것을 확인합니다.

글: https://copyandrun.com/blog/hermes-agent-local-ollama/

## 파일

- `docker-compose.yml`
- `Dockerfile`
- `Modelfile.qwen25-3b-64k`
- `Modelfile.qwen3-27b-64k`

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
