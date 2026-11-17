# Lynis로 리눅스 하드닝 점수 올려 보기: 우분투 컨테이너 보완 전후와 점수 게이트

새 우분투 24.04 컨테이너를 Lynis 3.0.9로 점검해 하드닝 점수 57과 제안 39개를 확인하고, 패키지 설치와 설정 보완 스크립트를 적용해 점수 70과 제안 25개로 비교합니다. 사라진 제안과 새로 생긴 제안을 대조하고, 한글 배너가 통하지 않은 이유와 점수만 믿으면 안 되는 점까지 확인합니다.

## 링크

- 글: [https://copyandrun.com/blog/lynis-container-host-audit/](https://copyandrun.com/blog/lynis-container-host-audit/)
- 한 번에 받기: [lynis-container-host-audit.zip](https://copyandrun.com/code-zip/lynis-container-host-audit.zip)
- GitHub 폴더: [copyandrun-labs/lynis-container-host-audit](https://github.com/fankh/copyandrun-labs/tree/main/lynis-container-host-audit)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `lynis_demo.sh` | <a href="https://fankh.github.io/copyandrun-labs/lynis-container-host-audit/lynis_demo.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/lynis-container-host-audit/lynis_demo.sh) |
| `lynis_fix.sh` | <a href="https://fankh.github.io/copyandrun-labs/lynis-container-host-audit/lynis_fix.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/lynis-container-host-audit/lynis_fix.sh) |
| `lynis_summary.py` | <a href="https://fankh.github.io/copyandrun-labs/lynis-container-host-audit/lynis_summary.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/lynis-container-host-audit/lynis_summary.py) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
