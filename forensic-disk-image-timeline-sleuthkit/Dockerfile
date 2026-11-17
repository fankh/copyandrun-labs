FROM debian:bookworm-slim
RUN apt-get update \
 && apt-get install -y --no-install-recommends sleuthkit e2fsprogs python3 \
 && rm -rf /var/lib/apt/lists/*
ENV TZ=UTC
WORKDIR /work
