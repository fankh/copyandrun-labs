# Dockle로 만들어진 컨테이너 이미지 점검하기: 비밀 노출, root 실행, 종료 코드 기준까지

일부러 나쁘게 만든 이미지와 고친 이미지를 Dockle로 점검합니다. CIS-DI 지적을 하나씩 읽고, 베이스 이미지에서 나오는 오탐을 예외로 두고, 이미지 기록에서 ENV 비밀이 그대로 읽히는 것과 종료 코드 기준(--exit-level)을 실행해 확인합니다.

글: https://copyandrun.com/blog/dockle-image-best-practice-check/

## 파일

- `app.py`
- `Dockerfile.bad`
- `Dockerfile.good`
- `dockle_demo.sh`

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
