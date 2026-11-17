# PwnKit 점검: pkexec 버전이 0.105여도 패치됐는지 변경 이력으로 확인하기

CVE-2021-4034(PwnKit)는 polkit 0.121 미만이 영향 범위지만, 배포판은 0.105 표기를 유지한 채 수정을 되돌려 반영합니다. 우분투 20.04 컨테이너에서 pkexec 표시 버전, 패키지 버전, SUID 비트, 변경 이력을 한 번에 확인하는 스크립트를 만듭니다.

## 링크

- 글: [https://copyandrun.com/blog/pwnkit-pkexec-patched-version-check/](https://copyandrun.com/blog/pwnkit-pkexec-patched-version-check/)
- 한 번에 받기: [pwnkit-pkexec-patched-version-check.zip](https://copyandrun.com/code-zip/pwnkit-pkexec-patched-version-check.zip)
- GitHub 폴더: [copyandrun-labs/pwnkit-pkexec-patched-version-check](https://github.com/fankh/copyandrun-labs/tree/main/pwnkit-pkexec-patched-version-check)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `pwnkit-check.sh` | <a href="https://fankh.github.io/copyandrun-labs/pwnkit-pkexec-patched-version-check/pwnkit-check.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/pwnkit-pkexec-patched-version-check/pwnkit-check.sh) |
| `pwnkit-lab.sh` | <a href="https://fankh.github.io/copyandrun-labs/pwnkit-pkexec-patched-version-check/pwnkit-lab.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/pwnkit-pkexec-patched-version-check/pwnkit-lab.sh) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
