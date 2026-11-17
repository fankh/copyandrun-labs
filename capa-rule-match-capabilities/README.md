# capa로 실행 파일의 기능 규칙 맞춰 보기: 어떤 동작을 근거로 판단하는지

Mandiant의 capa로 직접 컴파일한 시험 프로그램 세 개를 실행하지 않고 분석합니다. 규칙 이름, ATT&CK와 MBC 항목, 함수 주소와 API 근거를 읽고, JSON 결과를 파이썬으로 표로 요약합니다. capa가 기능의 존재를 알려 줄 뿐 악성 여부는 판정하지 않는다는 점도 결과로 확인합니다.

글: https://copyandrun.com/blog/capa-rule-match-capabilities/

## 파일

- `build.sh`
- `empty.c`
- `fileio.c`
- `run_capa.sh`
- `setup.sh`
- `sockdemo.c`
- `summarize.py`

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
