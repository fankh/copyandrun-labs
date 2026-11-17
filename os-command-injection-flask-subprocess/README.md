# OS 명령어 인젝션: ping 기능으로 보는 shell=True의 위험과 수정

호스트 ping 점검 화면만 있는 작은 Flask 도구에서 shell=True와 문자열 결합이 입력 한 줄로 서버 명령 실행까지 이어지는 과정을 id 출력으로 확인합니다. 인자 리스트, shell 미사용, ipaddress 검증, 허용 대역으로 고친 뒤 같은 입력이 거부되는 것까지 보고, 이 수정으로도 남는 한계를 짚습니다.

## 링크

- 글: [https://copyandrun.com/blog/os-command-injection-flask-subprocess/](https://copyandrun.com/blog/os-command-injection-flask-subprocess/)
- 한 번에 받기: [os-command-injection-flask-subprocess.zip](https://copyandrun.com/code-zip/os-command-injection-flask-subprocess.zip)
- GitHub 폴더: [copyandrun-labs/os-command-injection-flask-subprocess](https://github.com/fankh/copyandrun-labs/tree/main/os-command-injection-flask-subprocess)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `Dockerfile` | <a href="https://fankh.github.io/copyandrun-labs/os-command-injection-flask-subprocess/Dockerfile" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/os-command-injection-flask-subprocess/Dockerfile) |
| `ping_fixed.py` | <a href="https://fankh.github.io/copyandrun-labs/os-command-injection-flask-subprocess/ping_fixed.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/os-command-injection-flask-subprocess/ping_fixed.py) |
| `ping_vulnerable.py` | <a href="https://fankh.github.io/copyandrun-labs/os-command-injection-flask-subprocess/ping_vulnerable.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/os-command-injection-flask-subprocess/ping_vulnerable.py) |
| `requirements.txt` | <a href="https://fankh.github.io/copyandrun-labs/os-command-injection-flask-subprocess/requirements.txt" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/os-command-injection-flask-subprocess/requirements.txt) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
