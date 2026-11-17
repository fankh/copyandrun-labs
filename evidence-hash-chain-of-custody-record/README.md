# 증거 파일 해시와 보관 기록(chain of custody) 만들기

파이썬 표준 라이브러리만으로 증거 등록, 인계 기록, 검증을 하는 작은 도구를 만듭니다. 각 기록이 앞 기록의 SHA-256 해시를 포함하는 JSONL 체인을 쌓고, 파일 1바이트 변조와 기록 한 줄 변조가 각각 어디서 검증 실패로 드러나는지 실행해 봅니다.

## 링크

- 글: [https://copyandrun.com/blog/evidence-hash-chain-of-custody-record/](https://copyandrun.com/blog/evidence-hash-chain-of-custody-record/)
- 한 번에 받기: [evidence-hash-chain-of-custody-record.zip](https://copyandrun.com/code-zip/evidence-hash-chain-of-custody-record.zip)
- GitHub 폴더: [copyandrun-labs/evidence-hash-chain-of-custody-record](https://github.com/fankh/copyandrun-labs/tree/main/evidence-hash-chain-of-custody-record)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `custody.py` | <a href="https://fankh.github.io/copyandrun-labs/evidence-hash-chain-of-custody-record/custody.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/evidence-hash-chain-of-custody-record/custody.py) |
| `Dockerfile` | <a href="https://fankh.github.io/copyandrun-labs/evidence-hash-chain-of-custody-record/Dockerfile" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/evidence-hash-chain-of-custody-record/Dockerfile) |
| `make_evidence.py` | <a href="https://fankh.github.io/copyandrun-labs/evidence-hash-chain-of-custody-record/make_evidence.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/evidence-hash-chain-of-custody-record/make_evidence.py) |
| `tamper.py` | <a href="https://fankh.github.io/copyandrun-labs/evidence-hash-chain-of-custody-record/tamper.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/evidence-hash-chain-of-custody-record/tamper.py) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
