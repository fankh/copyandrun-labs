FROM python:3.12-slim
RUN apt-get update \
 && apt-get install -y --no-install-recommends gcc-mingw-w64-x86-64 \
 && rm -rf /var/lib/apt/lists/* \
 && pip install --no-cache-dir pefile
WORKDIR /work
