# Uptime Kuma로 서비스 상태 감시하기: 도커 실행, 감시 대상 추가, 정상과 장애 확인

오픈소스 모니터링 도구 Uptime Kuma를 도커로 localhost에만 열어 띄우고, 감시 대상 두 개를 등록해 정상(UP)과 장애(DOWN)가 각각 기록되는 것을 확인합니다. 데이터가 도커 볼륨에 남는 방식도 함께 봅니다.

## 링크

- 글: [https://copyandrun.com/blog/uptime-kuma-docker-monitor/](https://copyandrun.com/blog/uptime-kuma-docker-monitor/)
- 한 번에 받기: [uptime-kuma-docker-monitor.zip](https://copyandrun.com/code-zip/uptime-kuma-docker-monitor.zip)
- GitHub 폴더: [copyandrun-labs/uptime-kuma-docker-monitor](https://github.com/fankh/copyandrun-labs/tree/main/uptime-kuma-docker-monitor)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `kuma_demo.py` | <a href="https://fankh.github.io/copyandrun-labs/uptime-kuma-docker-monitor/kuma_demo.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/uptime-kuma-docker-monitor/kuma_demo.py) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
