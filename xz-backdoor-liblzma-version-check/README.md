# XZ 백도어 점검: xz 버전 5.6.0, 5.6.1 여부와 sshd의 liblzma 연결 확인하기

XZ 백도어(CVE-2024-3094)는 xz 5.6.0과 5.6.1 릴리스에 들어 있었습니다. 설치된 xz 버전을 확인하고, sshd가 liblzma를 불러오는지 ldd로 점검하는 스크립트를 만들어 우분투 22.04 컨테이너에서 실행합니다.

글: https://copyandrun.com/blog/xz-backdoor-liblzma-version-check/

## 파일

- `xz-check.sh`
- `xz-lab.sh`

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
