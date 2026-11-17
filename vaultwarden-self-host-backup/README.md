# Vaultwarden으로 비밀번호 관리 서버 띄우기: 도커 실행, 상태 확인, 데이터 백업

Bitwarden과 호환되는 오픈소스 서버 Vaultwarden을 도커로 localhost에만 열어 띄우고, 상태 확인 주소와 데이터 파일을 살펴봅니다. 컨테이너를 멈추고 데이터베이스를 복사해 백업한 뒤 다시 시작해도 서버가 살아나는지 확인합니다.

## 링크

- 글: [https://copyandrun.com/blog/vaultwarden-self-host-backup/](https://copyandrun.com/blog/vaultwarden-self-host-backup/)
- 한 번에 받기: [vaultwarden-self-host-backup.zip](https://copyandrun.com/code-zip/vaultwarden-self-host-backup.zip)
- GitHub 폴더: [copyandrun-labs/vaultwarden-self-host-backup](https://github.com/fankh/copyandrun-labs/tree/main/vaultwarden-self-host-backup)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `vw_test.py` | <a href="https://fankh.github.io/copyandrun-labs/vaultwarden-self-host-backup/vw_test.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/vaultwarden-self-host-backup/vw_test.py) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
