# Zeek으로 pcap 읽어 conn.log와 http.log 만들기: 스캔 흔적과 404 개수 게이트

내 PC의 웹 컨테이너 트래픽을 pcap으로 저장하고 Zeek 9.0.1로 읽어 JSON 로그를 만든 뒤, 정상 요청과 스캔 요청을 비교합니다. Zeek의 패킷 합계를 tcpdump 개수와 대조하고, 한 출발지의 404가 기준을 넘으면 종료 코드 1로 끝나는 게이트까지 만듭니다.

글: https://copyandrun.com/blog/zeek-pcap-conn-http-logs/

## 파일

- `nginx_lab.conf`
- `zeek_demo.sh`
- `zeek_summary.py`

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
