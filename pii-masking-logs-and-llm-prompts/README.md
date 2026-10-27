# 로그와 LLM 프롬프트의 개인정보 마스킹: 주민번호·전화번호 패턴과 점검표

Flask 앱의 로그와 LLM 호출 직전 프롬프트에 가짜 주민등록번호 형식, 휴대전화, 이메일, 카드번호가 그대로 남는 것을 OpenSearch Dashboards 로 확인하고, logging.Filter 와 프롬프트 전처리, Luhn 체크섬 검증으로 가린 뒤 다시 비교합니다.

글: https://copyandrun.com/blog/pii-masking-logs-and-llm-prompts/

## 파일

- `app.py`
- `check_leaks.py`
- `docker-compose.yml`
- `mock_llm.py`
- `pii.py`
- `send_traffic.py`
- `setup.py`
- `ship_logs.py`
- `test_pii.py`

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
