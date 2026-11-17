# Syft로 컨테이너 이미지의 SBOM 만들기: 패키지 목록을 파일로 남기는 법

오픈소스 도구 Syft를 도커로 실행해 python:3.9-alpine 이미지의 구성 요소 목록을 만들고, CycloneDX JSON으로 저장해 항목 종류별로 세어 봅니다. 목록만 있으면 나중에 새로 알려진 취약점과 다시 맞춰 볼 수 있다는 점까지 확인합니다.

## 링크

- 글: [https://copyandrun.com/blog/syft-sbom-container-image/](https://copyandrun.com/blog/syft-sbom-container-image/)
- 한 번에 받기: [syft-sbom-container-image.zip](https://copyandrun.com/code-zip/syft-sbom-container-image.zip)
- GitHub 폴더: [copyandrun-labs/syft-sbom-container-image](https://github.com/fankh/copyandrun-labs/tree/main/syft-sbom-container-image)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `count.py` | <a href="https://fankh.github.io/copyandrun-labs/syft-sbom-container-image/count.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/syft-sbom-container-image/count.py) |
| `make_sbom.sh` | <a href="https://fankh.github.io/copyandrun-labs/syft-sbom-container-image/make_sbom.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/syft-sbom-container-image/make_sbom.sh) |
| `syft_more.sh` | <a href="https://fankh.github.io/copyandrun-labs/syft-sbom-container-image/syft_more.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/syft-sbom-container-image/syft_more.sh) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
