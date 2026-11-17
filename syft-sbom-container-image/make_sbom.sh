#!/usr/bin/env bash
# Syft 로 컨테이너 이미지의 패키지 목록을 표와 CycloneDX JSON(SBOM)으로 만들고 종류별로 센다.
# 준비: Docker, 파이썬. Syft 는 설치하지 않고 컨테이너로 실행한다.
# 실행: bash make_sbom.sh   (같은 폴더에 sbom.json 이 만들어진다)
set -u
IMAGE_TABLE=python:3.12-alpine
IMAGE_SBOM=python:3.9-alpine

echo "## 1. 사람이 읽는 표(앞 10줄)"
docker run --rm anchore/syft:latest "$IMAGE_TABLE" -o table 2>/dev/null | head -10

echo "## 2. 저장용 SBOM(CycloneDX JSON)"
docker run --rm anchore/syft:latest "$IMAGE_SBOM" -o cyclonedx-json > sbom.json 2>/dev/null
ls -l sbom.json | awk '{print $5, "bytes", $9}'

echo "## 3. 종류별로 세기"
python -X utf8 count.py
