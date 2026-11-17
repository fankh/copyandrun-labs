# Loki로 nginx 로그 모으고 LogQL로 조회하기: 라벨 설계와 개인정보 마스킹

nginx 접근 로그 하나를 Promtail 설정 두 개로 Loki 두 대에 보냅니다. 요청 주소와 IP를 라벨로 만든 나쁜 설정은 스트림이 11개로 늘고 이메일과 토큰이 그대로 저장되며, 좋은 설정은 스트림 1개에 마스킹된 줄만 저장합니다. 5xx 개수와 401 반복 IP를 LogQL로 세고, 점검 결과를 종료 코드로 바꿉니다.

글: https://copyandrun.com/blog/loki-promtail-log-query-logql/

## 파일

- `lbc_check.py`
- `lbc_peek.py`
- `loki_bad.yaml`
- `loki_demo.sh`
- `loki_good.yaml`
- `loki_peek.sh`
- `nginx_lab.conf`
- `promtail_bad.yaml`
- `promtail_good.yaml`

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
