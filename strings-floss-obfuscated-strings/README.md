# strings와 FLOSS로 문자열 꺼내기: 평문, 인코딩, 실행 중에 조립하는 문자열

직접 만든 무해한 PE 파일에 평문, UTF-16, XOR, base64, 스택 조립 문자열을 넣고 strings와 FLOSS로 무엇이 보이고 안 보이는지 비교합니다. 파일은 실행하지 않고 열어서 읽기만 합니다.

글: https://copyandrun.com/blog/strings-floss-obfuscated-strings/

## 파일

- `decode_xor.py`
- `demo.c`
- `Dockerfile`
- `gen_encoded.py`
- `run.sh`

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
