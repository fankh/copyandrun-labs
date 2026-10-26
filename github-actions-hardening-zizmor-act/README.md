# GitHub Actions 워크플로 하드닝: 위험 패턴 찾고 고치기

일부러 취약하게 만든 워크플로를 zizmor로 점검해 여섯 건을 찾고, 커밋 SHA 고정과 권한 최소화 등으로 고쳐 0건이 되는지 확인합니다. act로 수정본이 로컬에서 도는지도 시험합니다.

글: https://copyandrun.com/blog/github-actions-hardening-zizmor-act/

## 파일

- `calc.py`
- `event.json`
- `fixed-ci.yml`
- `inject-demo.yml`
- `sample-ci.yml`
- `test_calc.py`
- `viewer.py`

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
