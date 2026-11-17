#!/usr/bin/env bash
# KEEP=1 bash loki_demo.sh 로 남겨 둔 두 Loki 의 라벨과 저장된 줄을 보고, 컨테이너를 지운다.
export MSYS_NO_PATHCONV=1
HERE="$(pwd)"
docker run --rm --network osk-lbc-net -v "$HERE:/w:ro" python:3.12-slim python /w/lbc_peek.py
docker rm -f osk-lbc-web osk-lbc-loki-bad osk-lbc-loki-good osk-lbc-pt-bad osk-lbc-pt-good osk-lbc-ca osk-lbc-cb >/dev/null 2>&1
docker network rm osk-lbc-net >/dev/null
