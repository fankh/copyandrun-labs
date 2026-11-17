# ELK 스냅샷과 이미지로 백업하고 복구하기

Elasticsearch 스냅샷으로 데이터를, 컨테이너 이미지로 설치 상태를 따로 보관합니다. 인덱스를 지운 뒤 복원해 보며 백업이 동작하는지 확인합니다.

## 링크

- 글: [https://copyandrun.com/blog/elk-snapshot-backup/](https://copyandrun.com/blog/elk-snapshot-backup/)
- 한 번에 받기: [elk-snapshot-backup.zip](https://copyandrun.com/code-zip/elk-snapshot-backup.zip)
- GitHub 폴더: [copyandrun-labs/elk-snapshot-backup](https://github.com/fankh/copyandrun-labs/tree/main/elk-snapshot-backup)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `fix-file-changed.sh` | <a href="https://fankh.github.io/copyandrun-labs/elk-snapshot-backup/fix-file-changed.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/elk-snapshot-backup/fix-file-changed.sh) |
| `recover-from-image.sh` | <a href="https://fankh.github.io/copyandrun-labs/elk-snapshot-backup/recover-from-image.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/elk-snapshot-backup/recover-from-image.sh) |
| `restore-check.sh` | <a href="https://fankh.github.io/copyandrun-labs/elk-snapshot-backup/restore-check.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/elk-snapshot-backup/restore-check.sh) |
| `snapshot-backup.sh` | <a href="https://fankh.github.io/copyandrun-labs/elk-snapshot-backup/snapshot-backup.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/elk-snapshot-backup/snapshot-backup.sh) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
