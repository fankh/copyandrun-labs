# sops와 age로 설정 파일의 비밀만 암호화하기: 저장소에 올려도 되는 비밀 관리

설정 파일에서 비밀번호와 토큰 값만 암호화해 파일 구조는 그대로 읽히게 하는 sops를 age 키와 함께 실행합니다. 복호화, 키가 없을 때와 틀릴 때, 파일 변조 감지, 값 수정 시 바뀌는 줄, 팀원 키 추가까지 확인합니다.

## 링크

- 글: [https://copyandrun.com/blog/sops-age-encrypted-config/](https://copyandrun.com/blog/sops-age-encrypted-config/)
- 한 번에 받기: [sops-age-encrypted-config.zip](https://copyandrun.com/code-zip/sops-age-encrypted-config.zip)
- GitHub 폴더: [copyandrun-labs/sops-age-encrypted-config](https://github.com/fankh/copyandrun-labs/tree/main/sops-age-encrypted-config)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `sops_demo.sh` | <a href="https://fankh.github.io/copyandrun-labs/sops-age-encrypted-config/sops_demo.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/sops-age-encrypted-config/sops_demo.sh) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
