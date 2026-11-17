# strings와 FLOSS로 문자열 꺼내기: 평문, 인코딩, 실행 중에 조립하는 문자열

직접 만든 무해한 PE 파일에 평문, UTF-16, XOR, base64, 스택 조립 문자열을 넣고 strings와 FLOSS로 무엇이 보이고 안 보이는지 비교합니다. 파일은 실행하지 않고 열어서 읽기만 합니다.

## 링크

- 글: [https://copyandrun.com/blog/strings-floss-obfuscated-strings/](https://copyandrun.com/blog/strings-floss-obfuscated-strings/)
- 한 번에 받기: [strings-floss-obfuscated-strings.zip](https://copyandrun.com/code-zip/strings-floss-obfuscated-strings.zip)
- GitHub 폴더: [copyandrun-labs/strings-floss-obfuscated-strings](https://github.com/fankh/copyandrun-labs/tree/main/strings-floss-obfuscated-strings)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `decode_xor.py` | <a href="https://fankh.github.io/copyandrun-labs/strings-floss-obfuscated-strings/decode_xor.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/strings-floss-obfuscated-strings/decode_xor.py) |
| `demo.c` | <a href="https://fankh.github.io/copyandrun-labs/strings-floss-obfuscated-strings/demo.c" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/strings-floss-obfuscated-strings/demo.c) |
| `Dockerfile` | <a href="https://fankh.github.io/copyandrun-labs/strings-floss-obfuscated-strings/Dockerfile" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/strings-floss-obfuscated-strings/Dockerfile) |
| `gen_encoded.py` | <a href="https://fankh.github.io/copyandrun-labs/strings-floss-obfuscated-strings/gen_encoded.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/strings-floss-obfuscated-strings/gen_encoded.py) |
| `run.sh` | <a href="https://fankh.github.io/copyandrun-labs/strings-floss-obfuscated-strings/run.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/strings-floss-obfuscated-strings/run.sh) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
