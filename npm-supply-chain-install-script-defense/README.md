# npm 설치 때 실행되는 스크립트를 막고 락파일 바뀐 곳 찾기

내 로컬 npm 레지스트리 Verdaccio에 무해한 패키지 둘을 올려 postinstall이 설치 때 실행되는 것을 재현하고, ignore-scripts와 npm rebuild로 막습니다. 이어서 package-lock.json에서 resolved와 integrity가 바뀐 줄, 예상 밖 레지스트리, 새로 생긴 설치 스크립트를 찾는 보고서를 만들고 npm audit signatures와 최소 버전 나이 정책도 시험합니다.

## 링크

- 글: [https://copyandrun.com/blog/npm-supply-chain-install-script-defense/](https://copyandrun.com/blog/npm-supply-chain-install-script-defense/)
- 한 번에 받기: [npm-supply-chain-install-script-defense.zip](https://copyandrun.com/code-zip/npm-supply-chain-install-script-defense.zip)
- GitHub 폴더: [copyandrun-labs/npm-supply-chain-install-script-defense](https://github.com/fankh/copyandrun-labs/tree/main/npm-supply-chain-install-script-defense)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `age_policy.sh` | <a href="https://fankh.github.io/copyandrun-labs/npm-supply-chain-install-script-defense/age_policy.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/npm-supply-chain-install-script-defense/age_policy.sh) |
| `compare_view.py` | <a href="https://fankh.github.io/copyandrun-labs/npm-supply-chain-install-script-defense/compare_view.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/npm-supply-chain-install-script-defense/compare_view.py) |
| `docker-compose.yml` | <a href="https://fankh.github.io/copyandrun-labs/npm-supply-chain-install-script-defense/docker-compose.yml" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/npm-supply-chain-install-script-defense/docker-compose.yml) |
| `lockdiff.py` | <a href="https://fankh.github.io/copyandrun-labs/npm-supply-chain-install-script-defense/lockdiff.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/npm-supply-chain-install-script-defense/lockdiff.py) |
| `make_app.sh` | <a href="https://fankh.github.io/copyandrun-labs/npm-supply-chain-install-script-defense/make_app.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/npm-supply-chain-install-script-defense/make_app.sh) |
| `make_packages.sh` | <a href="https://fankh.github.io/copyandrun-labs/npm-supply-chain-install-script-defense/make_packages.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/npm-supply-chain-install-script-defense/make_packages.sh) |
| `run_defense.sh` | <a href="https://fankh.github.io/copyandrun-labs/npm-supply-chain-install-script-defense/run_defense.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/npm-supply-chain-install-script-defense/run_defense.sh) |
| `tamper_lock.py` | <a href="https://fankh.github.io/copyandrun-labs/npm-supply-chain-install-script-defense/tamper_lock.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/npm-supply-chain-install-script-defense/tamper_lock.py) |
| `verdaccio-config.yaml` | <a href="https://fankh.github.io/copyandrun-labs/npm-supply-chain-install-script-defense/verdaccio-config.yaml" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/npm-supply-chain-install-script-defense/verdaccio-config.yaml) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
