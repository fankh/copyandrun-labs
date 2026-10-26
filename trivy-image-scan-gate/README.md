# Trivy로 컨테이너 이미지 취약점을 스캔하고 빌드 게이트 만들기

오래된 베이스 이미지와 고정 버전 패키지로 작은 이미지를 빌드해 Trivy로 스캔하고, 결과 표 읽는 법과 HIGH,CRITICAL 필터, --ignore-unfixed, --exit-code 1 게이트, 만료일이 있는 .trivyignore 예외를 거쳐 베이스 이미지를 올려 통과시킵니다.

글: https://copyandrun.com/blog/trivy-image-scan-gate/

## 파일

- `app.py`
- `Dockerfile`
- `Dockerfile.fixed`
- `gate_view.py`
- `requirements.fixed.txt`
- `requirements.txt`
- `trivy-scan.yml`
- `trivyignore-flask`
- `trivyignore-pip`

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
