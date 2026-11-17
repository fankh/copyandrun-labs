# 엔트로피와 섹션 이름으로 패킹된 파일 가려내기: UPX 전후 비교

무해한 시험 프로그램을 UPX로 압축해 원본과 섹션 이름, 섹션별 엔트로피, 임포트 수, 크기를 pefile과 직접 짠 Shannon 엔트로피로 비교합니다. 임계값 스크립트로 목록을 거르고, zip과 이미지가 오탐으로 걸리는 모습과 upx -d 해제 결과를 실행 결과로 확인합니다.

글: https://copyandrun.com/blog/entropy-upx-packed-detect/

## 파일

- `Dockerfile`
- `entropy_report.py`
- `hello.c`
- `make_samples.py`
- `scan_packed.py`

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
