# OS 명령어 인젝션: ping 기능으로 보는 shell=True의 위험과 수정

호스트 ping 점검 화면만 있는 작은 Flask 도구에서 shell=True와 문자열 결합이 입력 한 줄로 서버 명령 실행까지 이어지는 과정을 id 출력으로 확인합니다. 인자 리스트, shell 미사용, ipaddress 검증, 허용 대역으로 고친 뒤 같은 입력이 거부되는 것까지 보고, 이 수정으로도 남는 한계를 짚습니다.

글: https://copyandrun.com/blog/os-command-injection-flask-subprocess/

## 파일

- `Dockerfile`
- `ping_fixed.py`
- `ping_vulnerable.py`
- `requirements.txt`

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
