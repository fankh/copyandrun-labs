# pefile로 실행 파일 구조 읽기: 헤더, 섹션, 임포트 표에서 보이는 것

무해한 C 프로그램을 mingw-w64로 Windows 실행 파일(PE)로 컴파일만 하고, 파이썬 pefile로 DOS와 NT 헤더, 섹션 권한, 임포트 표, 컴파일 시각, 서브시스템을 읽습니다. 임포트 함수가 주는 단서와 임포트만으로 단정하면 안 되는 이유를 실행 결과로 확인합니다.

## 링크

- 글: [https://copyandrun.com/blog/pe-header-imports-pefile-read/](https://copyandrun.com/blog/pe-header-imports-pefile-read/)
- 한 번에 받기: [pe-header-imports-pefile-read.zip](https://copyandrun.com/code-zip/pe-header-imports-pefile-read.zip)
- GitHub 폴더: [copyandrun-labs/pe-header-imports-pefile-read](https://github.com/fankh/copyandrun-labs/tree/main/pe-header-imports-pefile-read)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `build.sh` | <a href="https://fankh.github.io/copyandrun-labs/pe-header-imports-pefile-read/build.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/pe-header-imports-pefile-read/build.sh) |
| `Dockerfile` | <a href="https://fankh.github.io/copyandrun-labs/pe-header-imports-pefile-read/Dockerfile" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/pe-header-imports-pefile-read/Dockerfile) |
| `find_clues.py` | <a href="https://fankh.github.io/copyandrun-labs/pe-header-imports-pefile-read/find_clues.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/pe-header-imports-pefile-read/find_clues.py) |
| `read_pe.py` | <a href="https://fankh.github.io/copyandrun-labs/pe-header-imports-pefile-read/read_pe.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/pe-header-imports-pefile-read/read_pe.py) |
| `sample.c` | <a href="https://fankh.github.io/copyandrun-labs/pe-header-imports-pefile-read/sample.c" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/pe-header-imports-pefile-read/sample.c) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
