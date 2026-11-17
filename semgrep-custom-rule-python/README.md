# Semgrep으로 우리 팀 규칙 만들기: 파이썬 사용자 규칙 여섯 개와 규칙 시험

Semgrep 규칙 여섯 개(SQL 문자열 조립, 인증서 검증 끄기, 약한 해시, 요청값이 셸로 흐르는 taint, shell=True, 팀 전용 함수 금지)를 직접 쓰고 semgrep --test로 시험한 뒤, 약한 코드와 고친 코드에 적용해 종료 코드 게이트를 만듭니다. bandit과 비교하고 규칙을 일부러 깨서 시험이 잡는지도 확인합니다.

글: https://copyandrun.com/blog/semgrep-custom-rule-python/

## 파일

- `bad_app.py`
- `company.py`
- `company.yml`
- `good_app.py`
- `semgrep_demo.sh`
- `semgrep_summary.py`

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
