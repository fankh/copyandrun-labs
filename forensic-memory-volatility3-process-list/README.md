# Volatility 3 메모리 덤프 프로세스 목록 읽기: pslist, pstree

공개된 윈도우 XP 메모리 이미지 두 개에 Volatility 3 의 windows.info, pslist, pstree, psscan 을 실행해 프로세스 목록을 읽습니다. 세 결과를 비교하고, ExitTime 이 찍힌 종료 프로세스와 PID, PPID 로 읽는 부모 자식 관계, 비정상 부모를 점검하는 위치를 파이썬 요약 스크립트로 정리합니다.

글: https://copyandrun.com/blog/forensic-memory-volatility3-process-list/

## 파일

- `Dockerfile`
- `fetch_images.sh`
- `process_report.py`
- `run_vol.sh`
- `short.awk`

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
