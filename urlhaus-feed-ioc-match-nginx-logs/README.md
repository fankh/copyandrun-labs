# URLhaus IOC 피드와 nginx 로그 대조하기

공개 IOC 피드를 로그와 대조하는 방법을 다룹니다. abuse.ch URLhaus의 이용 조건(인증키, 내려받기 간격)을 문서로 확인하고, 시험용 nginx 로그를 가짜 IOC 목록과 대조해 일치와 오탐을 가려내는 스크립트를 만듭니다. 키 없이 받을 수 있는 Feodo Tracker 피드로 실제 목록 대조와 갱신 시각 점검도 해 보며, URLhaus 피드 본문은 인증키가 없어 받지 않았습니다.

## 링크

- 글: [https://copyandrun.com/blog/urlhaus-feed-ioc-match-nginx-logs/](https://copyandrun.com/blog/urlhaus-feed-ioc-match-nginx-logs/)
- 한 번에 받기: [urlhaus-feed-ioc-match-nginx-logs.zip](https://copyandrun.com/code-zip/urlhaus-feed-ioc-match-nginx-logs.zip)
- GitHub 폴더: [copyandrun-labs/urlhaus-feed-ioc-match-nginx-logs](https://github.com/fankh/copyandrun-labs/tree/main/urlhaus-feed-ioc-match-nginx-logs)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `allowlist.txt` | <a href="https://fankh.github.io/copyandrun-labs/urlhaus-feed-ioc-match-nginx-logs/allowlist.txt" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/urlhaus-feed-ioc-match-nginx-logs/allowlist.txt) |
| `Dockerfile` | <a href="https://fankh.github.io/copyandrun-labs/urlhaus-feed-ioc-match-nginx-logs/Dockerfile" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/urlhaus-feed-ioc-match-nginx-logs/Dockerfile) |
| `fake_iocs.txt` | <a href="https://fankh.github.io/copyandrun-labs/urlhaus-feed-ioc-match-nginx-logs/fake_iocs.txt" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/urlhaus-feed-ioc-match-nginx-logs/fake_iocs.txt) |
| `ioc_match.py` | <a href="https://fankh.github.io/copyandrun-labs/urlhaus-feed-ioc-match-nginx-logs/ioc_match.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/urlhaus-feed-ioc-match-nginx-logs/ioc_match.py) |
| `make_logs.sh` | <a href="https://fankh.github.io/copyandrun-labs/urlhaus-feed-ioc-match-nginx-logs/make_logs.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/urlhaus-feed-ioc-match-nginx-logs/make_logs.sh) |
| `nginx.conf` | <a href="https://fankh.github.io/copyandrun-labs/urlhaus-feed-ioc-match-nginx-logs/nginx.conf" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/urlhaus-feed-ioc-match-nginx-logs/nginx.conf) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
