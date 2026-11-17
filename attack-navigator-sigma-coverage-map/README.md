# ATT&CK Navigator로 Sigma 탐지 규칙 범위 그리기

Sigma 규칙의 tags(attack.t1059.001 등)를 파이썬으로 읽어 기법별 규칙 개수를 세고, ATT&CK Navigator 레이어(JSON)로 저장해 로컬 Navigator 화면에서 열어 봅니다. 규칙이 없는 전술 칸과 이름이 바뀐 기법 ID를 찾아내는 방법, 그리고 규칙 개수가 탐지 품질을 뜻하지 않는다는 한계까지 다룹니다.

글: https://copyandrun.com/blog/attack-navigator-sigma-coverage-map/

## 파일

- `Dockerfile`
- `sample_rules.yml`
- `sigma_to_layer.py`

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
