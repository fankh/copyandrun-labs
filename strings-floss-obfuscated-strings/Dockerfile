FROM python:3.12-slim-bookworm
RUN apt-get update \
 && apt-get install -y --no-install-recommends gcc-mingw-w64-x86-64-win32 binutils file g++ \
 && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir flare-floss
WORKDIR /work
COPY demo.c decode_xor.py gen_encoded.py run.sh ./
