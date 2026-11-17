# Volatility 3 메모리 덤프 프로세스 목록 읽기: pslist, pstree

공개된 윈도우 XP 메모리 이미지 두 개에 Volatility 3 의 windows.info, pslist, pstree, psscan 을 실행해 프로세스 목록을 읽습니다. 세 결과를 비교하고, ExitTime 이 찍힌 종료 프로세스와 PID, PPID 로 읽는 부모 자식 관계, 비정상 부모를 점검하는 위치를 파이썬 요약 스크립트로 정리합니다.

## 링크

- 글: [https://copyandrun.com/blog/forensic-memory-volatility3-process-list/](https://copyandrun.com/blog/forensic-memory-volatility3-process-list/)
- 한 번에 받기: [forensic-memory-volatility3-process-list.zip](https://copyandrun.com/code-zip/forensic-memory-volatility3-process-list.zip)
- GitHub 폴더: [copyandrun-labs/forensic-memory-volatility3-process-list](https://github.com/fankh/copyandrun-labs/tree/main/forensic-memory-volatility3-process-list)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `Dockerfile` | <a href="https://fankh.github.io/copyandrun-labs/forensic-memory-volatility3-process-list/Dockerfile" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/forensic-memory-volatility3-process-list/Dockerfile) |
| `fetch_images.sh` | <a href="https://fankh.github.io/copyandrun-labs/forensic-memory-volatility3-process-list/fetch_images.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/forensic-memory-volatility3-process-list/fetch_images.sh) |
| `process_report.py` | <a href="https://fankh.github.io/copyandrun-labs/forensic-memory-volatility3-process-list/process_report.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/forensic-memory-volatility3-process-list/process_report.py) |
| `run_vol.sh` | <a href="https://fankh.github.io/copyandrun-labs/forensic-memory-volatility3-process-list/run_vol.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/forensic-memory-volatility3-process-list/run_vol.sh) |
| `short.awk` | <a href="https://fankh.github.io/copyandrun-labs/forensic-memory-volatility3-process-list/short.awk" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/forensic-memory-volatility3-process-list/short.awk) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
