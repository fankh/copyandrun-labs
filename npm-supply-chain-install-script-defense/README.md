# npm 설치 때 실행되는 스크립트를 막고 락파일 바뀐 곳 찾기

내 로컬 npm 레지스트리 Verdaccio에 무해한 패키지 둘을 올려 postinstall이 설치 때 실행되는 것을 재현하고, ignore-scripts와 npm rebuild로 막습니다. 이어서 package-lock.json에서 resolved와 integrity가 바뀐 줄, 예상 밖 레지스트리, 새로 생긴 설치 스크립트를 찾는 보고서를 만들고 npm audit signatures와 최소 버전 나이 정책도 시험합니다.

글: https://copyandrun.com/blog/npm-supply-chain-install-script-defense/

## 파일

- `age_policy.sh`
- `compare_view.py`
- `docker-compose.yml`
- `lockdiff.py`
- `make_app.sh`
- `make_packages.sh`
- `run_defense.sh`
- `tamper_lock.py`
- `verdaccio-config.yaml`

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
