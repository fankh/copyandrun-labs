# AIDE로 파일 무결성 기준선 만들고 변경 감지하기: 수정, 권한, 삭제, 추가와 기준선 바꿔치기

AIDE 0.18.6으로 설정 폴더의 해시와 권한 기준선을 만들고, 내용 수정, 권한 변경, 삭제와 추가, 수정 시각만 바꾼 경우를 점검해 종료 코드 비트를 읽는 게이트로 바꿉니다. 공격자가 기준선 DB를 다시 만들면 변경이 사라지는 점과 DB 해시를 밖에 적어 두는 방어까지 확인합니다.

## 링크

- 글: [https://copyandrun.com/blog/aide-file-integrity-baseline/](https://copyandrun.com/blog/aide-file-integrity-baseline/)
- 한 번에 받기: [aide-file-integrity-baseline.zip](https://copyandrun.com/code-zip/aide-file-integrity-baseline.zip)
- GitHub 폴더: [copyandrun-labs/aide-file-integrity-baseline](https://github.com/fankh/copyandrun-labs/tree/main/aide-file-integrity-baseline)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `aide_demo.sh` | <a href="https://fankh.github.io/copyandrun-labs/aide-file-integrity-baseline/aide_demo.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/aide-file-integrity-baseline/aide_demo.sh) |
| `aide_gate.sh` | <a href="https://fankh.github.io/copyandrun-labs/aide-file-integrity-baseline/aide_gate.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/aide-file-integrity-baseline/aide_gate.sh) |
| `lab.conf` | <a href="https://fankh.github.io/copyandrun-labs/aide-file-integrity-baseline/lab.conf" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/aide-file-integrity-baseline/lab.conf) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
