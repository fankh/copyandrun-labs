# ELK를 직접 설치할 빈 우분투 서버
FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=C.UTF-8

# 저장소 등록, 상태 확인, 편집에 필요한 도구만 넣습니다(ELK는 넣지 않습니다)
RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates curl gnupg apt-transport-https sudo \
        procps less nano vim-tiny python3 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /labs

# 컨테이너가 꺼지지 않게 대기합니다
CMD ["sleep", "infinity"]
