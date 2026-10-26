#!/usr/bin/env bash
# 배포 전 게이트: 서명(과 선택적으로 SBOM 증명)이 맞아야 종료 코드 0, 아니면 1.
# 사용법: ./verify_gate.sh <이미지 참조> [공개키 파일]
#   REQUIRE_SBOM=1 ./verify_gate.sh localhost:5390/demo/hello@sha256:...
set -u
cd "$(dirname "$0")"
. ./lab.sh

REF="${1:?usage: verify_gate.sh <image-ref> [public-key]}"
PUB="${2:-cosign.pub}"

if ! cosign verify --key "$PUB" --insecure-ignore-tlog=true "$REF" >/tmp/gate-verify.out 2>&1; then
  echo "GATE FAIL  signature  $REF"
  grep -E "^Error|no signatures|no matching" /tmp/gate-verify.out | head -3
  exit 1
fi
echo "GATE PASS  signature  $REF"

if [ "${REQUIRE_SBOM:-0}" = "1" ]; then
  if ! cosign verify-attestation --key "$PUB" --insecure-ignore-tlog=true \
       --type cyclonedx "$REF" >/tmp/gate-att.out 2>&1; then
    echo "GATE FAIL  sbom       $REF"
    grep -E "^Error|none of the attestations" /tmp/gate-att.out | head -3
    exit 1
  fi
  echo "GATE PASS  sbom       $REF"
fi

# 검증을 통과한 다이제스트를 알려 줍니다. 배포는 태그가 아니라 이 값으로 합니다.
DIGEST="$(grep -o '"docker-manifest-digest":"sha256:[0-9a-f]*"' /tmp/gate-verify.out | head -1 | cut -d'"' -f4)"
NAME="${REF%%@*}"                  # @sha256:... 제거
LAST="${NAME##*/}"
NAME="${NAME%/*}/${LAST%%:*}"         # :태그 제거
echo "DEPLOY     ${NAME}@${DIGEST}"
exit 0
