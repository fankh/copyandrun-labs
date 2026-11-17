# 우리 사무실 네트워크에 열린 서비스 점검: nmap으로 기기별 포트 표 만들고 줄이기

Docker 사설 네트워크에 프린터, NAS, 공유기, 일반 PC를 흉내 낸 컨테이너를 띄우고, 자기 소유 대역만 nmap으로 점검해 기기별 열린 포트를 표로 정리합니다. telnet, 평문 FTP, 관리 화면을 우선순위로 읽고, 쓰지 않는 서비스를 끈 뒤 다시 점검해 6개가 3개로 줄어드는 것을 확인합니다.

글: https://copyandrun.com/blog/home-office-network-nmap-open-services-check/

## 파일

- `device.py`
- `Dockerfile`
- `lab_down.sh`
- `lab_up.sh`
- `scan.sh`
- `scan_table.py`

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
