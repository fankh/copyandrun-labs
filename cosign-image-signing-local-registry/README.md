# 컨테이너 이미지에 서명하고 서명 없는 이미지 거부하기(cosign)

내 컴퓨터의 로컬 레지스트리에 작은 이미지를 올리고 cosign으로 서명해 검증합니다. SBOM 증명을 붙이고, 같은 태그로 다른 이미지를 덮어쓰면 검증이 실패하는 것과 서명 없는 이미지가 거부되는 것을 재현한 뒤, 다이제스트로 고정해 배포하는 게이트 스크립트로 마무리합니다.

## 링크

- 글: [https://copyandrun.com/blog/cosign-image-signing-local-registry/](https://copyandrun.com/blog/cosign-image-signing-local-registry/)
- 한 번에 받기: [cosign-image-signing-local-registry.zip](https://copyandrun.com/code-zip/cosign-image-signing-local-registry.zip)
- GitHub 폴더: [copyandrun-labs/cosign-image-signing-local-registry](https://github.com/fankh/copyandrun-labs/tree/main/cosign-image-signing-local-registry)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `app.py` | <a href="https://fankh.github.io/copyandrun-labs/cosign-image-signing-local-registry/app.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/cosign-image-signing-local-registry/app.py) |
| `cosign.pub` | <a href="https://fankh.github.io/copyandrun-labs/cosign-image-signing-local-registry/cosign.pub" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/cosign-image-signing-local-registry/cosign.pub) |
| `docker-compose.yml` | <a href="https://fankh.github.io/copyandrun-labs/cosign-image-signing-local-registry/docker-compose.yml" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/cosign-image-signing-local-registry/docker-compose.yml) |
| `Dockerfile` | <a href="https://fankh.github.io/copyandrun-labs/cosign-image-signing-local-registry/Dockerfile" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/cosign-image-signing-local-registry/Dockerfile) |
| `lab.sh` | <a href="https://fankh.github.io/copyandrun-labs/cosign-image-signing-local-registry/lab.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/cosign-image-signing-local-registry/lab.sh) |
| `verify_gate.sh` | <a href="https://fankh.github.io/copyandrun-labs/cosign-image-signing-local-registry/verify_gate.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/cosign-image-signing-local-registry/verify_gate.sh) |
| `view.py` | <a href="https://fankh.github.io/copyandrun-labs/cosign-image-signing-local-registry/view.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/cosign-image-signing-local-registry/view.py) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
