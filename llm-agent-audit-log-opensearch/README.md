# 에이전트가 한 일을 추적하는 감사 로그: 호출마다 실행 주체와 도구를 남기기

에이전트들이 서비스 계정 하나로 도구를 부르면 누가 무엇을 했는지 로그에 남지 않습니다. 호출마다 agent_id, session_id, run_id 를 붙여 OpenSearch 에 색인하고, Dashboards 에서 호출 순서를 재구성하고 승인 없는 삭제를 잡아냅니다.

## 링크

- 글: [https://copyandrun.com/blog/llm-agent-audit-log-opensearch/](https://copyandrun.com/blog/llm-agent-audit-log-opensearch/)
- 한 번에 받기: [llm-agent-audit-log-opensearch.zip](https://copyandrun.com/code-zip/llm-agent-audit-log-opensearch.zip)
- GitHub 폴더: [copyandrun-labs/llm-agent-audit-log-opensearch](https://github.com/fankh/copyandrun-labs/tree/main/llm-agent-audit-log-opensearch)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `app.py` | <a href="https://fankh.github.io/copyandrun-labs/llm-agent-audit-log-opensearch/app.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/llm-agent-audit-log-opensearch/app.py) |
| `calls.py` | <a href="https://fankh.github.io/copyandrun-labs/llm-agent-audit-log-opensearch/calls.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/llm-agent-audit-log-opensearch/calls.py) |
| `detect_unapproved_delete.py` | <a href="https://fankh.github.io/copyandrun-labs/llm-agent-audit-log-opensearch/detect_unapproved_delete.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/llm-agent-audit-log-opensearch/detect_unapproved_delete.py) |
| `docker-compose.yml` | <a href="https://fankh.github.io/copyandrun-labs/llm-agent-audit-log-opensearch/docker-compose.yml" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/llm-agent-audit-log-opensearch/docker-compose.yml) |
| `index_template.json` | <a href="https://fankh.github.io/copyandrun-labs/llm-agent-audit-log-opensearch/index_template.json" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/llm-agent-audit-log-opensearch/index_template.json) |
| `query_run.py` | <a href="https://fankh.github.io/copyandrun-labs/llm-agent-audit-log-opensearch/query_run.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/llm-agent-audit-log-opensearch/query_run.py) |
| `setup.py` | <a href="https://fankh.github.io/copyandrun-labs/llm-agent-audit-log-opensearch/setup.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/llm-agent-audit-log-opensearch/setup.py) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
