# sudoers 점검: NOPASSWD, 와일드카드, 셸 탈출 규칙 찾아 고치기

visudo가 문법 오류가 없다고 해도 sudoers 규칙이 안전하다는 뜻은 아닙니다. /etc/sudoers.d의 규칙에서 NOPASSWD, 모든 명령 허용, 와일드카드, 셸을 열 수 있는 편집기를 찾는 스크립트를 만들고, 시험 규칙 5건이 걸리는 것과 고친 뒤 0건이 되는 것을 확인합니다.

## 링크

- 글: [https://copyandrun.com/blog/sudoers-audit-nopasswd-wildcard/](https://copyandrun.com/blog/sudoers-audit-nopasswd-wildcard/)
- 한 번에 받기: [sudoers-audit-nopasswd-wildcard.zip](https://copyandrun.com/code-zip/sudoers-audit-nopasswd-wildcard.zip)
- GitHub 폴더: [copyandrun-labs/sudoers-audit-nopasswd-wildcard](https://github.com/fankh/copyandrun-labs/tree/main/sudoers-audit-nopasswd-wildcard)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `sudoers-audit.sh` | <a href="https://fankh.github.io/copyandrun-labs/sudoers-audit-nopasswd-wildcard/sudoers-audit.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/sudoers-audit-nopasswd-wildcard/sudoers-audit.sh) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
