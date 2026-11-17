# CI에 Semgrep과 Bandit 보안 게이트 붙이기

Bandit과 Semgrep을 GitHub Actions에서 돌려 심각도 기준으로 빌드를 실패시키는 설정을 만듭니다. 같은 검사를 로컬에서 먼저 돌려 종료 코드로 통과와 실패를 확인합니다.

## 링크

- 글: [https://copyandrun.com/blog/ci-semgrep-bandit-gate/](https://copyandrun.com/blog/ci-semgrep-bandit-gate/)
- 한 번에 받기: [ci-semgrep-bandit-gate.zip](https://copyandrun.com/code-zip/ci-semgrep-bandit-gate.zip)
- GitHub 폴더: [copyandrun-labs/ci-semgrep-bandit-gate](https://github.com/fankh/copyandrun-labs/tree/main/ci-semgrep-bandit-gate)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `Jenkinsfile` | <a href="https://fankh.github.io/copyandrun-labs/ci-semgrep-bandit-gate/Jenkinsfile" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/ci-semgrep-bandit-gate/Jenkinsfile) |
| `main-fixed.py` | <a href="https://fankh.github.io/copyandrun-labs/ci-semgrep-bandit-gate/main-fixed.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/ci-semgrep-bandit-gate/main-fixed.py) |
| `main.py` | <a href="https://fankh.github.io/copyandrun-labs/ci-semgrep-bandit-gate/main.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/ci-semgrep-bandit-gate/main.py) |
| `no-shell-true.yml` | <a href="https://fankh.github.io/copyandrun-labs/ci-semgrep-bandit-gate/no-shell-true.yml" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/ci-semgrep-bandit-gate/no-shell-true.yml) |
| `report_view.py` | <a href="https://fankh.github.io/copyandrun-labs/ci-semgrep-bandit-gate/report_view.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/ci-semgrep-bandit-gate/report_view.py) |
| `sast.yml` | <a href="https://fankh.github.io/copyandrun-labs/ci-semgrep-bandit-gate/sast.yml" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/ci-semgrep-bandit-gate/sast.yml) |
| `semgrep.sh` | <a href="https://fankh.github.io/copyandrun-labs/ci-semgrep-bandit-gate/semgrep.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/ci-semgrep-bandit-gate/semgrep.sh) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
