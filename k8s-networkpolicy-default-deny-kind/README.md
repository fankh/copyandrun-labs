# Kubernetes NetworkPolicy 기본 거부: kind로 허용과 차단 확인

kind 클러스터에서 파드끼리 아무 제한 없이 통신하는 것을 확인하고, 네임스페이스 전체에 기본 거부 정책을 건 뒤 웹에서 DB로 가는 길만 허용합니다. 파드 안에서 실제로 연결해 보는 점검 화면으로 적용 전, 기본 거부만 건 상태, 허용을 더한 상태를 비교합니다.

글: https://copyandrun.com/blog/k8s-networkpolicy-default-deny-kind/

## 파일

- `00-apps.yaml`
- `10-default-deny.yaml`
- `20-allow.yaml`
- `kind-config.yaml`
- `view.py`

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
