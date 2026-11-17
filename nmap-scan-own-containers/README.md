# Nmap으로 내 컨테이너 포트 점검하기: 열린 포트, 버전 확인, 스크립트 한 줄

도커 전용 네트워크에 만든 시험용 nginx 컨테이너를 Nmap으로 점검합니다. 1~1024번 포트 중 열린 포트 찾기, 서비스 버전 확인, http-title과 http-headers 스크립트 결과를 읽고, 허락받은 대상만 스캔해야 하는 이유를 정리합니다.

## 링크

- 글: [https://copyandrun.com/blog/nmap-scan-own-containers/](https://copyandrun.com/blog/nmap-scan-own-containers/)
- 한 번에 받기: [nmap-scan-own-containers.zip](https://copyandrun.com/code-zip/nmap-scan-own-containers.zip)
- GitHub 폴더: [copyandrun-labs/nmap-scan-own-containers](https://github.com/fankh/copyandrun-labs/tree/main/nmap-scan-own-containers)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `scan_lab.sh` | <a href="https://fankh.github.io/copyandrun-labs/nmap-scan-own-containers/scan_lab.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/nmap-scan-own-containers/scan_lab.sh) |
| `scan_more.sh` | <a href="https://fankh.github.io/copyandrun-labs/nmap-scan-own-containers/scan_more.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/nmap-scan-own-containers/scan_more.sh) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
