# SPF, DKIM, DMARC 기록 읽고 점검하기: 파이썬

컨테이너 안의 dnsmasq에 example.test 영역을 만들어 SPF, DKIM, DMARC 기록을 정상, 느슨함, 조회 10회 초과, 기록 중복, 문법 오류로 나눠 직접 올리고, dnspython 스크립트로 조회 횟수를 세고 오류를 짚어 정책을 요약합니다. 외부 DNS는 조회하지 않고 메일도 보내지 않습니다.

글: https://copyandrun.com/blog/spf-dkim-dmarc-record-check-local-dns/

## 파일

- `check_mail_dns.py`
- `dnsmasq.conf`
- `Dockerfile`
- `show_txt.py`

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
