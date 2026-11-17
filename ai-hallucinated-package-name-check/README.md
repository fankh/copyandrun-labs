# AI가 지어낸 패키지 이름 가려내기: 설치 전 PyPI 조회와 CI 게이트

AI가 써 준 requirements.txt의 각 이름이 PyPI에 실제로 있는지, 최초 릴리스가 너무 최근은 아닌지, 릴리스가 몇 개인지, 널리 쓰는 이름과 비슷하지는 않은지를 JSON API 조회만으로 점검하는 파이썬 스크립트를 만듭니다. 종료 코드로 CI 게이트를 걸고, 로컬 가짜 인덱스로 신규 패키지 경우도 시험합니다.

## 링크

- 글: [https://copyandrun.com/blog/ai-hallucinated-package-name-check/](https://copyandrun.com/blog/ai-hallucinated-package-name-check/)
- 한 번에 받기: [ai-hallucinated-package-name-check.zip](https://copyandrun.com/code-zip/ai-hallucinated-package-name-check.zip)
- GitHub 폴더: [copyandrun-labs/ai-hallucinated-package-name-check](https://github.com/fankh/copyandrun-labs/tree/main/ai-hallucinated-package-name-check)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `allowlist.txt` | <a href="https://fankh.github.io/copyandrun-labs/ai-hallucinated-package-name-check/allowlist.txt" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/ai-hallucinated-package-name-check/allowlist.txt) |
| `Dockerfile` | <a href="https://fankh.github.io/copyandrun-labs/ai-hallucinated-package-name-check/Dockerfile" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/ai-hallucinated-package-name-check/Dockerfile) |
| `fake_index.py` | <a href="https://fankh.github.io/copyandrun-labs/ai-hallucinated-package-name-check/fake_index.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/ai-hallucinated-package-name-check/fake_index.py) |
| `gate.sh` | <a href="https://fankh.github.io/copyandrun-labs/ai-hallucinated-package-name-check/gate.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/ai-hallucinated-package-name-check/gate.sh) |
| `pkgcheck.py` | <a href="https://fankh.github.io/copyandrun-labs/ai-hallucinated-package-name-check/pkgcheck.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/ai-hallucinated-package-name-check/pkgcheck.py) |
| `popular.txt` | <a href="https://fankh.github.io/copyandrun-labs/ai-hallucinated-package-name-check/popular.txt" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/ai-hallucinated-package-name-check/popular.txt) |
| `requirements-fake.txt` | <a href="https://fankh.github.io/copyandrun-labs/ai-hallucinated-package-name-check/requirements-fake.txt" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/ai-hallucinated-package-name-check/requirements-fake.txt) |
| `requirements.txt` | <a href="https://fankh.github.io/copyandrun-labs/ai-hallucinated-package-name-check/requirements.txt" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/ai-hallucinated-package-name-check/requirements.txt) |
| `warn-only.txt` | <a href="https://fankh.github.io/copyandrun-labs/ai-hallucinated-package-name-check/warn-only.txt" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/ai-hallucinated-package-name-check/warn-only.txt) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
