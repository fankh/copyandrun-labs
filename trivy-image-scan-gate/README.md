# Trivy로 컨테이너 이미지 취약점을 스캔하고 빌드 게이트 만들기

오래된 베이스 이미지와 고정 버전 패키지로 작은 이미지를 빌드해 Trivy로 스캔하고, 결과 표 읽는 법과 HIGH,CRITICAL 필터, --ignore-unfixed, --exit-code 1 게이트, 만료일이 있는 .trivyignore 예외를 거쳐 베이스 이미지를 올려 통과시킵니다.

## 링크

- 글: [https://copyandrun.com/blog/trivy-image-scan-gate/](https://copyandrun.com/blog/trivy-image-scan-gate/)
- 한 번에 받기: [trivy-image-scan-gate.zip](https://copyandrun.com/code-zip/trivy-image-scan-gate.zip)
- GitHub 폴더: [copyandrun-labs/trivy-image-scan-gate](https://github.com/fankh/copyandrun-labs/tree/main/trivy-image-scan-gate)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `app.py` | <a href="https://fankh.github.io/copyandrun-labs/trivy-image-scan-gate/app.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/trivy-image-scan-gate/app.py) |
| `Dockerfile` | <a href="https://fankh.github.io/copyandrun-labs/trivy-image-scan-gate/Dockerfile" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/trivy-image-scan-gate/Dockerfile) |
| `Dockerfile.fixed` | <a href="https://fankh.github.io/copyandrun-labs/trivy-image-scan-gate/Dockerfile.fixed" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/trivy-image-scan-gate/Dockerfile.fixed) |
| `gate_view.py` | <a href="https://fankh.github.io/copyandrun-labs/trivy-image-scan-gate/gate_view.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/trivy-image-scan-gate/gate_view.py) |
| `requirements.fixed.txt` | <a href="https://fankh.github.io/copyandrun-labs/trivy-image-scan-gate/requirements.fixed.txt" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/trivy-image-scan-gate/requirements.fixed.txt) |
| `requirements.txt` | <a href="https://fankh.github.io/copyandrun-labs/trivy-image-scan-gate/requirements.txt" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/trivy-image-scan-gate/requirements.txt) |
| `trivy-scan.yml` | <a href="https://fankh.github.io/copyandrun-labs/trivy-image-scan-gate/trivy-scan.yml" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/trivy-image-scan-gate/trivy-scan.yml) |
| `trivyignore-flask` | <a href="https://fankh.github.io/copyandrun-labs/trivy-image-scan-gate/trivyignore-flask" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/trivy-image-scan-gate/trivyignore-flask) |
| `trivyignore-pip` | <a href="https://fankh.github.io/copyandrun-labs/trivy-image-scan-gate/trivyignore-pip" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/trivy-image-scan-gate/trivyignore-pip) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
