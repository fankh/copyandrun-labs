# 실습용 도구 함수. 다른 스크립트가 source 해서 씁니다.
# cosign, syft 를 설치하지 않고 Docker 이미지로 실행합니다.
# --network container:cr-t10-registry 는 레지스트리 컨테이너와 네트워크를 공유해서
# 컨테이너 안에서도 localhost:5390 으로 같은 레지스트리에 닿게 합니다.
REGISTRY=localhost:5390
COSIGN_IMG=ghcr.io/sigstore/cosign/cosign:v3.1.4@sha256:0f06154836d2de34f887a5c273506d52ca43edaa1d9e53e6510fa78a48f69c2d
SYFT_IMG=anchore/syft:v1.55.0@sha256:4cc92b64ca74ffca4c94d4c8fcc01f217731375300be14d0b6eeb2e82eaa110a

cosign() {
  MSYS_NO_PATHCONV=1 docker run --rm --user "$(id -u):$(id -g)" --tmpfs /tmp:rw,mode=1777 --network container:cr-t10-registry \
    -v "$PWD:/work" -w /work -e HOME=/tmp -e COSIGN_PASSWORD "$COSIGN_IMG" "$@"
}

syft() {
  MSYS_NO_PATHCONV=1 docker run --rm --user "$(id -u):$(id -g)" --tmpfs /tmp:rw,mode=1777 --network container:cr-t10-registry \
    -e HOME=/tmp -e SYFT_REGISTRY_INSECURE_USE_HTTP=true \
    -v "$PWD:/work" -w /work "$SYFT_IMG" "$@"
}
