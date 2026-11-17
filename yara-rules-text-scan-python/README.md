# YARA 룰 작성과 파이썬 스캔: 문자열 조건으로 파일 분류하기

yara-python으로 룰 두 개를 만들어 샘플 세 개를 스캔합니다. any of them과 all of them 조건의 차이, 문자열 출현 횟수 조건, 룰 문법 오류 메시지를 실행 결과로 확인하고, 문자열 기반 룰의 한계를 정리합니다.

## 링크

- 글: [https://copyandrun.com/blog/yara-rules-text-scan-python/](https://copyandrun.com/blog/yara-rules-text-scan-python/)
- 한 번에 받기: [yara-rules-text-scan-python.zip](https://copyandrun.com/code-zip/yara-rules-text-scan-python.zip)
- GitHub 폴더: [copyandrun-labs/yara-rules-text-scan-python](https://github.com/fankh/copyandrun-labs/tree/main/yara-rules-text-scan-python)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `rules.yar` | <a href="https://fankh.github.io/copyandrun-labs/yara-rules-text-scan-python/rules.yar" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/yara-rules-text-scan-python/rules.yar) |
| `scan.py` | <a href="https://fankh.github.io/copyandrun-labs/yara-rules-text-scan-python/scan.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/yara-rules-text-scan-python/scan.py) |
| `yara_more.py` | <a href="https://fankh.github.io/copyandrun-labs/yara-rules-text-scan-python/yara_more.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/yara-rules-text-scan-python/yara_more.py) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
