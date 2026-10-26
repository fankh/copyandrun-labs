FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
 && apt-get install -y --no-install-recommends curl git ca-certificates tar xz-utils sudo less procps tmux \
 && rm -rf /var/lib/apt/lists/*

# 에이전트는 일반 사용자로 실행합니다.
RUN useradd -m -s /bin/bash agent \
 && echo "agent ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/agent
USER agent
WORKDIR /home/agent
ENV PATH="/home/agent/.local/bin:${PATH}"

# 브라우저 도구는 이 실습에서 쓰지 않으므로 건너뜁니다.
RUN curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash -s -- --non-interactive --skip-browser --skip-computer-use

# 연습용 폴더입니다. 컨테이너 안에서 에이전트가 만지는 파일은 여기에만 둡니다.
RUN mkdir -p /home/agent/practice

CMD ["bash"]
