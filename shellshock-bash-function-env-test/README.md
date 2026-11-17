# Shellshock 점검: bash 환경 변수 함수 정의 뒤의 명령이 실행되는지 안전하게 확인하기

Shellshock(CVE-2014-6271)은 bash가 환경 변수의 함수 정의 뒤에 붙은 문자열까지 실행한 취약점입니다. echo 한 줄만 붙인 환경 변수로 bash 3.2, 4.3, 5.2를 점검하고, 취약한 경우의 판정은 시험용 가짜 bash로 확인합니다.

## 링크

- 글: [https://copyandrun.com/blog/shellshock-bash-function-env-test/](https://copyandrun.com/blog/shellshock-bash-function-env-test/)
- 한 번에 받기: [shellshock-bash-function-env-test.zip](https://copyandrun.com/code-zip/shellshock-bash-function-env-test.zip)
- GitHub 폴더: [copyandrun-labs/shellshock-bash-function-env-test](https://github.com/fankh/copyandrun-labs/tree/main/shellshock-bash-function-env-test)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `fake-bash.sh` | <a href="https://fankh.github.io/copyandrun-labs/shellshock-bash-function-env-test/fake-bash.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/shellshock-bash-function-env-test/fake-bash.sh) |
| `shellshock-check.sh` | <a href="https://fankh.github.io/copyandrun-labs/shellshock-bash-function-env-test/shellshock-check.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/shellshock-bash-function-env-test/shellshock-check.sh) |
| `shellshock-lab.sh` | <a href="https://fankh.github.io/copyandrun-labs/shellshock-bash-function-env-test/shellshock-lab.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/shellshock-bash-function-env-test/shellshock-lab.sh) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
