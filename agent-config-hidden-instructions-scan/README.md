# 저장소의 에이전트 설정 파일에 숨은 지시 찾아내기

AGENTS.md 같은 에이전트 규칙 파일에 보이지 않는 유니코드, HTML 주석, 외부 전송 명령 문구, base64 덩어리로 숨긴 지시를 파이썬 스캐너로 찾아 복원합니다. 종료 코드로 pre-commit 훅과 GitHub Actions 게이트를 만들고, 눈에 보이는 평문 지시나 다른 인코딩을 놓치는 한계도 실제 실행 결과로 확인합니다.

## 링크

- 글: [https://copyandrun.com/blog/agent-config-hidden-instructions-scan/](https://copyandrun.com/blog/agent-config-hidden-instructions-scan/)
- 한 번에 받기: [agent-config-hidden-instructions-scan.zip](https://copyandrun.com/code-zip/agent-config-hidden-instructions-scan.zip)
- GitHub 폴더: [copyandrun-labs/agent-config-hidden-instructions-scan](https://github.com/fankh/copyandrun-labs/tree/main/agent-config-hidden-instructions-scan)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `agent-config-scan.yml` | <a href="https://fankh.github.io/copyandrun-labs/agent-config-hidden-instructions-scan/agent-config-scan.yml" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/agent-config-hidden-instructions-scan/agent-config-scan.yml) |
| `agent_config_scan.py` | <a href="https://fankh.github.io/copyandrun-labs/agent-config-hidden-instructions-scan/agent_config_scan.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/agent-config-hidden-instructions-scan/agent_config_scan.py) |
| `limits_check.py` | <a href="https://fankh.github.io/copyandrun-labs/agent-config-hidden-instructions-scan/limits_check.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/agent-config-hidden-instructions-scan/limits_check.py) |
| `make_samples.py` | <a href="https://fankh.github.io/copyandrun-labs/agent-config-hidden-instructions-scan/make_samples.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/agent-config-hidden-instructions-scan/make_samples.py) |
| `pre-commit-config.yaml` | <a href="https://fankh.github.io/copyandrun-labs/agent-config-hidden-instructions-scan/pre-commit-config.yaml" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/agent-config-hidden-instructions-scan/pre-commit-config.yaml) |
| `viewer_app.py` | <a href="https://fankh.github.io/copyandrun-labs/agent-config-hidden-instructions-scan/viewer_app.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/agent-config-hidden-instructions-scan/viewer_app.py) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
