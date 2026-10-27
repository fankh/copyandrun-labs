# Open WebUI를 Docker로 띄워 Ollama에 연결하고 모델이 안 보일 때 고치기

Docker로 Open WebUI를 띄워 호스트의 Ollama에 연결하고, 주소를 localhost로 잘못 넣어 모델 목록이 비는 상태를 만든 뒤 원인을 찾아 고칩니다. 환경 변수를 바로잡아도 저장된 설정이 우선해 되돌아오지 않는 동작도 직접 확인합니다.

글: https://copyandrun.com/blog/open-webui-ollama-connect-fix/

## 파일

- `check-ollama.sh`
- `docker-compose.yml`

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
