# 우리 사무실 네트워크에 열린 서비스 점검: nmap으로 기기별 포트 표 만들고 줄이기

Docker 사설 네트워크에 프린터, NAS, 공유기, 일반 PC를 흉내 낸 컨테이너를 띄우고, 자기 소유 대역만 nmap으로 점검해 기기별 열린 포트를 표로 정리합니다. telnet, 평문 FTP, 관리 화면을 우선순위로 읽고, 쓰지 않는 서비스를 끈 뒤 다시 점검해 6개가 3개로 줄어드는 것을 확인합니다.

## 링크

- 글: [https://copyandrun.com/blog/home-office-network-nmap-open-services-check/](https://copyandrun.com/blog/home-office-network-nmap-open-services-check/)
- 한 번에 받기: [home-office-network-nmap-open-services-check.zip](https://copyandrun.com/code-zip/home-office-network-nmap-open-services-check.zip)
- GitHub 폴더: [copyandrun-labs/home-office-network-nmap-open-services-check](https://github.com/fankh/copyandrun-labs/tree/main/home-office-network-nmap-open-services-check)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `device.py` | <a href="https://fankh.github.io/copyandrun-labs/home-office-network-nmap-open-services-check/device.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/home-office-network-nmap-open-services-check/device.py) |
| `Dockerfile` | <a href="https://fankh.github.io/copyandrun-labs/home-office-network-nmap-open-services-check/Dockerfile" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/home-office-network-nmap-open-services-check/Dockerfile) |
| `lab_down.sh` | <a href="https://fankh.github.io/copyandrun-labs/home-office-network-nmap-open-services-check/lab_down.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/home-office-network-nmap-open-services-check/lab_down.sh) |
| `lab_up.sh` | <a href="https://fankh.github.io/copyandrun-labs/home-office-network-nmap-open-services-check/lab_up.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/home-office-network-nmap-open-services-check/lab_up.sh) |
| `scan.sh` | <a href="https://fankh.github.io/copyandrun-labs/home-office-network-nmap-open-services-check/scan.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/home-office-network-nmap-open-services-check/scan.sh) |
| `scan_table.py` | <a href="https://fankh.github.io/copyandrun-labs/home-office-network-nmap-open-services-check/scan_table.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/home-office-network-nmap-open-services-check/scan_table.py) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
