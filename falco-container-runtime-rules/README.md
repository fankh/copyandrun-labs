# Falco 컨테이너 런타임 규칙 시험: 셸 실행, /etc 쓰기

Falco 0.45.2를 modern eBPF 드라이버로 Docker Desktop에서 띄우고 사용자 규칙 세 개를 얹어, 평범한 컨테이너와 수상한 동작을 한 컨테이너를 같은 방법으로 비교합니다. 처음에는 경고가 0건이었던 이유(준비 시간, 규칙 하나만 걸리는 기본 동작)를 풀고 결과를 종료 코드로 바꿉니다.

글: https://copyandrun.com/blog/falco-container-runtime-rules/

## 파일

- `falco_demo.sh`
- `falco_summary.py`
- `lab_rules.yaml`

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
