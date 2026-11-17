# Suricata로 pcap 파일 재생해 보기: 사용자 규칙과 alert 개수 게이트

내 PC의 웹 컨테이너 트래픽을 pcap으로 저장하고, Suricata 8.0.8이 그 파일을 읽어 평문 비밀번호 전송, 경로 이탈, 포트 스캔 규칙으로 alert를 내는지 정상 pcap과 공격 pcap으로 비교합니다. 규칙 하나가 조용히 0건이었던 이유와 alert 개수를 종료 코드로 바꾸는 방법까지 다룹니다.

## 링크

- 글: [https://copyandrun.com/blog/suricata-pcap-replay-alerts/](https://copyandrun.com/blog/suricata-pcap-replay-alerts/)
- 한 번에 받기: [suricata-pcap-replay-alerts.zip](https://copyandrun.com/code-zip/suricata-pcap-replay-alerts.zip)
- GitHub 폴더: [copyandrun-labs/suricata-pcap-replay-alerts](https://github.com/fankh/copyandrun-labs/tree/main/suricata-pcap-replay-alerts)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `local.rules` | <a href="https://fankh.github.io/copyandrun-labs/suricata-pcap-replay-alerts/local.rules" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/suricata-pcap-replay-alerts/local.rules) |
| `nginx_lab.conf` | <a href="https://fankh.github.io/copyandrun-labs/suricata-pcap-replay-alerts/nginx_lab.conf" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/suricata-pcap-replay-alerts/nginx_lab.conf) |
| `suricata_demo.sh` | <a href="https://fankh.github.io/copyandrun-labs/suricata-pcap-replay-alerts/suricata_demo.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/suricata-pcap-replay-alerts/suricata_demo.sh) |
| `suricata_summary.py` | <a href="https://fankh.github.io/copyandrun-labs/suricata-pcap-replay-alerts/suricata_summary.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/suricata-pcap-replay-alerts/suricata_summary.py) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
