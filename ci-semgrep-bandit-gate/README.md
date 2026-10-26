# CI에 Semgrep과 Bandit 보안 게이트 붙이기

Bandit과 Semgrep을 GitHub Actions에서 돌려 심각도 기준으로 빌드를 실패시키는 설정을 만듭니다. 같은 검사를 로컬에서 먼저 돌려 종료 코드로 통과와 실패를 확인합니다.

글: https://copyandrun.com/blog/ci-semgrep-bandit-gate/

## 파일

- `Jenkinsfile`
- `main-fixed.py`
- `main.py`
- `no-shell-true.yml`
- `report_view.py`
- `sast.yml`
- `semgrep.sh`

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
