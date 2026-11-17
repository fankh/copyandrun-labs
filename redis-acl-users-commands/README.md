# Redis ACL로 사용자별 명령과 키 제한하기

비밀번호 없는 default 사용자만 있는 Redis 7.4를 앱용과 읽기용 사용자로 나누고, default를 끄고, 키 패턴과 명령을 제한합니다. 같은 9칸짜리 허용/거부 표로 전후를 검사해 어긋난 칸이 6개에서 0개가 되는 것을 확인하고, 실행 없이 판정하는 ACL DRYRUN과 거부 사유를 남기는 ACL LOG로 교차 확인합니다.

## 링크

- 글: [https://copyandrun.com/blog/redis-acl-users-commands/](https://copyandrun.com/blog/redis-acl-users-commands/)
- 한 번에 받기: [redis-acl-users-commands.zip](https://copyandrun.com/code-zip/redis-acl-users-commands.zip)
- GitHub 폴더: [copyandrun-labs/redis-acl-users-commands](https://github.com/fankh/copyandrun-labs/tree/main/redis-acl-users-commands)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `redis_acl_demo.sh` | <a href="https://fankh.github.io/copyandrun-labs/redis-acl-users-commands/redis_acl_demo.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/redis-acl-users-commands/redis_acl_demo.sh) |
| `redis_cat_demo.sh` | <a href="https://fankh.github.io/copyandrun-labs/redis-acl-users-commands/redis_cat_demo.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/redis-acl-users-commands/redis_cat_demo.sh) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
