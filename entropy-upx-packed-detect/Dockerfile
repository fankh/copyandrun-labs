FROM python:3.12-slim-bookworm
RUN apt-get update \
 && apt-get install -y --no-install-recommends gcc-mingw-w64-x86-64 curl xz-utils ca-certificates \
 && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir pefile==2024.8.26
# UPX 공식 릴리스(리눅스 x86_64)를 받아 설치합니다.
RUN curl -fsSL -o /tmp/upx.tar.xz https://github.com/upx/upx/releases/download/v5.0.2/upx-5.0.2-amd64_linux.tar.xz \
 && tar -xJf /tmp/upx.tar.xz -C /tmp \
 && cp /tmp/upx-5.0.2-amd64_linux/upx /usr/local/bin/upx \
 && rm -rf /tmp/upx*
WORKDIR /work
