# Hadolint로 Dockerfile 점검하기: 열한 가지 지적을 읽고 고치고, CI 기준 정하기

일부러 나쁘게 쓴 Dockerfile을 Hadolint에 넣어 지적 열한 건을 규칙 번호별로 읽고 고칩니다. 실패 기준(--failure-threshold), 예외 설정, 고친 파일의 빌드와 실행 사용자까지 실행해 확인합니다.

## 링크

- 글: [https://copyandrun.com/blog/hadolint-dockerfile-lint/](https://copyandrun.com/blog/hadolint-dockerfile-lint/)
- 한 번에 받기: [hadolint-dockerfile-lint.zip](https://copyandrun.com/code-zip/hadolint-dockerfile-lint.zip)
- GitHub 폴더: [copyandrun-labs/hadolint-dockerfile-lint](https://github.com/fankh/copyandrun-labs/tree/main/hadolint-dockerfile-lint)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `app.py` | <a href="https://fankh.github.io/copyandrun-labs/hadolint-dockerfile-lint/app.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/hadolint-dockerfile-lint/app.py) |
| `Dockerfile.bad` | <a href="https://fankh.github.io/copyandrun-labs/hadolint-dockerfile-lint/Dockerfile.bad" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/hadolint-dockerfile-lint/Dockerfile.bad) |
| `Dockerfile.good` | <a href="https://fankh.github.io/copyandrun-labs/hadolint-dockerfile-lint/Dockerfile.good" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/hadolint-dockerfile-lint/Dockerfile.good) |
| `Dockerfile.warnonly` | <a href="https://fankh.github.io/copyandrun-labs/hadolint-dockerfile-lint/Dockerfile.warnonly" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/hadolint-dockerfile-lint/Dockerfile.warnonly) |
| `lint_demo.sh` | <a href="https://fankh.github.io/copyandrun-labs/hadolint-dockerfile-lint/lint_demo.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/hadolint-dockerfile-lint/lint_demo.sh) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
