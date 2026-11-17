#!/bin/sh
# 사용: sh run_server.sh app_v1 18270   (127.0.0.1 에만 바인딩합니다)
exec python -m uvicorn "$1:app" --host 127.0.0.1 --port "$2" --log-level warning
