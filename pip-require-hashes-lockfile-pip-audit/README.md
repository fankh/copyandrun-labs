# pip 의존성에 해시를 고정하고 취약점 점검하기

오래된 requests 를 pip-audit 로 점검해 수정 버전을 확인하고, pip-compile 로 해시 잠금 파일을 만들어 --require-hashes 로 설치합니다. 해시를 바꾸거나 빼면 설치가 멈추는 것, 로컬 인덱스에서 같은 이름과 버전의 내용이 바뀌어도 해시가 잡아내는 것, 의존성 혼동이 생기는 조건까지 내 컴퓨터 안에서 재현합니다.

## 링크

- 글: [https://copyandrun.com/blog/pip-require-hashes-lockfile-pip-audit/](https://copyandrun.com/blog/pip-require-hashes-lockfile-pip-audit/)
- 한 번에 받기: [pip-require-hashes-lockfile-pip-audit.zip](https://copyandrun.com/code-zip/pip-require-hashes-lockfile-pip-audit.zip)
- GitHub 폴더: [copyandrun-labs/pip-require-hashes-lockfile-pip-audit](https://github.com/fankh/copyandrun-labs/tree/main/pip-require-hashes-lockfile-pip-audit)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `docker-compose.yml` | <a href="https://fankh.github.io/copyandrun-labs/pip-require-hashes-lockfile-pip-audit/docker-compose.yml" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/pip-require-hashes-lockfile-pip-audit/docker-compose.yml) |
| `hash_check.py` | <a href="https://fankh.github.io/copyandrun-labs/pip-require-hashes-lockfile-pip-audit/hash_check.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/pip-require-hashes-lockfile-pip-audit/hash_check.py) |
| `lab.in` | <a href="https://fankh.github.io/copyandrun-labs/pip-require-hashes-lockfile-pip-audit/lab.in" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/pip-require-hashes-lockfile-pip-audit/lab.in) |
| `make_pkg.py` | <a href="https://fankh.github.io/copyandrun-labs/pip-require-hashes-lockfile-pip-audit/make_pkg.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/pip-require-hashes-lockfile-pip-audit/make_pkg.py) |
| `report_app.py` | <a href="https://fankh.github.io/copyandrun-labs/pip-require-hashes-lockfile-pip-audit/report_app.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/pip-require-hashes-lockfile-pip-audit/report_app.py) |
| `requirements-old.txt` | <a href="https://fankh.github.io/copyandrun-labs/pip-require-hashes-lockfile-pip-audit/requirements-old.txt" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/pip-require-hashes-lockfile-pip-audit/requirements-old.txt) |
| `requirements.in` | <a href="https://fankh.github.io/copyandrun-labs/pip-require-hashes-lockfile-pip-audit/requirements.in" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/pip-require-hashes-lockfile-pip-audit/requirements.in) |
| `tamper_lock.py` | <a href="https://fankh.github.io/copyandrun-labs/pip-require-hashes-lockfile-pip-audit/tamper_lock.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/pip-require-hashes-lockfile-pip-audit/tamper_lock.py) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
