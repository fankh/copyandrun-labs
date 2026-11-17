# Prometheus 알림 규칙 promtool 단위 시험

Prometheus 2.51 컨테이너의 promtool로 알림 규칙의 문법 오류와 논리 오류를 나눠 잡고, 가짜 시계열을 넣어 몇 분 뒤에 알림이 울리는지 단위 시험으로 확인합니다. Alertmanager 0.27의 amtool로 라벨별 수신처가 맞는지, 수신처를 빠뜨린 설정이 막히는지도 서버 없이 시험하고 종료 코드로 판정합니다.

## 링크

- 글: [https://copyandrun.com/blog/prometheus-alert-rules-promtool-test/](https://copyandrun.com/blog/prometheus-alert-rules-promtool-test/)
- 한 번에 받기: [prometheus-alert-rules-promtool-test.zip](https://copyandrun.com/code-zip/prometheus-alert-rules-promtool-test.zip)
- GitHub 폴더: [copyandrun-labs/prometheus-alert-rules-promtool-test](https://github.com/fankh/copyandrun-labs/tree/main/prometheus-alert-rules-promtool-test)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `alert_demo.sh` | <a href="https://fankh.github.io/copyandrun-labs/prometheus-alert-rules-promtool-test/alert_demo.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/prometheus-alert-rules-promtool-test/alert_demo.sh) |
| `am_bad.yml` | <a href="https://fankh.github.io/copyandrun-labs/prometheus-alert-rules-promtool-test/am_bad.yml" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/prometheus-alert-rules-promtool-test/am_bad.yml) |
| `am_good.yml` | <a href="https://fankh.github.io/copyandrun-labs/prometheus-alert-rules-promtool-test/am_good.yml" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/prometheus-alert-rules-promtool-test/am_good.yml) |
| `rules_bad.yml` | <a href="https://fankh.github.io/copyandrun-labs/prometheus-alert-rules-promtool-test/rules_bad.yml" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/prometheus-alert-rules-promtool-test/rules_bad.yml) |
| `rules_good.yml` | <a href="https://fankh.github.io/copyandrun-labs/prometheus-alert-rules-promtool-test/rules_good.yml" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/prometheus-alert-rules-promtool-test/rules_good.yml) |
| `rules_test.yml` | <a href="https://fankh.github.io/copyandrun-labs/prometheus-alert-rules-promtool-test/rules_test.yml" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/prometheus-alert-rules-promtool-test/rules_test.yml) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
