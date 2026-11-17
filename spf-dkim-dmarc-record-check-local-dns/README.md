# SPF, DKIM, DMARC 기록 읽고 점검하기: 파이썬

컨테이너 안의 dnsmasq에 example.test 영역을 만들어 SPF, DKIM, DMARC 기록을 정상, 느슨함, 조회 10회 초과, 기록 중복, 문법 오류로 나눠 직접 올리고, dnspython 스크립트로 조회 횟수를 세고 오류를 짚어 정책을 요약합니다. 외부 DNS는 조회하지 않고 메일도 보내지 않습니다.

## 링크

- 글: [https://copyandrun.com/blog/spf-dkim-dmarc-record-check-local-dns/](https://copyandrun.com/blog/spf-dkim-dmarc-record-check-local-dns/)
- 한 번에 받기: [spf-dkim-dmarc-record-check-local-dns.zip](https://copyandrun.com/code-zip/spf-dkim-dmarc-record-check-local-dns.zip)
- GitHub 폴더: [copyandrun-labs/spf-dkim-dmarc-record-check-local-dns](https://github.com/fankh/copyandrun-labs/tree/main/spf-dkim-dmarc-record-check-local-dns)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `check_mail_dns.py` | <a href="https://fankh.github.io/copyandrun-labs/spf-dkim-dmarc-record-check-local-dns/check_mail_dns.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/spf-dkim-dmarc-record-check-local-dns/check_mail_dns.py) |
| `dnsmasq.conf` | <a href="https://fankh.github.io/copyandrun-labs/spf-dkim-dmarc-record-check-local-dns/dnsmasq.conf" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/spf-dkim-dmarc-record-check-local-dns/dnsmasq.conf) |
| `Dockerfile` | <a href="https://fankh.github.io/copyandrun-labs/spf-dkim-dmarc-record-check-local-dns/Dockerfile" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/spf-dkim-dmarc-record-check-local-dns/Dockerfile) |
| `show_txt.py` | <a href="https://fankh.github.io/copyandrun-labs/spf-dkim-dmarc-record-check-local-dns/show_txt.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/spf-dkim-dmarc-record-check-local-dns/show_txt.py) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
