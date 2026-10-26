# 저장소의 에이전트 설정 파일에 숨은 지시 찾아내기

AGENTS.md 같은 에이전트 규칙 파일에 보이지 않는 유니코드, HTML 주석, 외부 전송 명령 문구, base64 덩어리로 숨긴 지시를 파이썬 스캐너로 찾아 복원합니다. 종료 코드로 pre-commit 훅과 GitHub Actions 게이트를 만들고, 눈에 보이는 평문 지시나 다른 인코딩을 놓치는 한계도 실제 실행 결과로 확인합니다.

글: https://copyandrun.com/blog/agent-config-hidden-instructions-scan/

## 파일

- `agent-config-scan.yml`
- `agent_config_scan.py`
- `limits_check.py`
- `make_samples.py`
- `pre-commit-config.yaml`
- `viewer_app.py`

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
