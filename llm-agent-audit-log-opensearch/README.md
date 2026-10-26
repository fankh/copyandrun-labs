# 에이전트가 한 일을 추적하는 감사 로그: 호출마다 실행 주체와 도구를 남기기

에이전트들이 서비스 계정 하나로 도구를 부르면 누가 무엇을 했는지 로그에 남지 않습니다. 호출마다 agent_id, session_id, run_id 를 붙여 OpenSearch 에 색인하고, Dashboards 에서 호출 순서를 재구성하고 승인 없는 삭제를 잡아냅니다.

글: https://copyandrun.com/blog/llm-agent-audit-log-opensearch/

## 파일

- `app.py`
- `calls.py`
- `detect_unapproved_delete.py`
- `docker-compose.yml`
- `index_template.json`
- `query_run.py`
- `setup.py`

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
