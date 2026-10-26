# ELK 스냅샷과 이미지로 백업하고 복구하기

Elasticsearch 스냅샷으로 데이터를, 컨테이너 이미지로 설치 상태를 따로 보관합니다. 인덱스를 지운 뒤 복원해 보며 백업이 동작하는지 확인합니다.

글: https://copyandrun.com/blog/elk-snapshot-backup/

## 파일

- `fix-file-changed.sh`
- `recover-from-image.sh`
- `restore-check.sh`
- `snapshot-backup.sh`

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
