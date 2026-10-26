FROM node:22-slim

ENV PYTHONUTF8=1 PYTHONIOENCODING=utf-8 LANG=C.UTF-8

RUN apt-get update \
 && apt-get install -y --no-install-recommends python3 python3-venv ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# 공식 MCP Python SDK 와 보고서 화면용 Flask 를 가상환경에 설치합니다.
RUN python3 -m venv /opt/venv \
 && /opt/venv/bin/pip install --no-cache-dir "mcp[cli]<2" flask
ENV PATH="/opt/venv/bin:${PATH}"

# MCP Inspector 는 도구 목록 화면을 눈으로 확인할 때만 씁니다.
RUN npm install -g @modelcontextprotocol/inspector

WORKDIR /lab
CMD ["sleep", "infinity"]
