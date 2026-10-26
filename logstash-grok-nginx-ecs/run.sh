#!/bin/bash
# 사용법: ./run.sh [logstash 추가 인자]   (입력은 표준입력 또는 file input)
MSYS_NO_PATHCONV=1 docker run --rm -i --name cr-logstash-run --network cr-logstash-net \
  -v "${PIPELINE_DIR:-$PWD/pipeline}:/usr/share/logstash/pipeline:ro" \
  -v "$PWD/logs:/data/logs:ro" \
  -e XPACK_MONITORING_ENABLED=false -e LS_JAVA_OPTS="-Xms512m -Xmx512m" \
  docker.elastic.co/logstash/logstash:8.19.0 --log.level error "$@" 2>&1 \
  | grep -v -E "^(Using bundled|Sending Logstash|[0-9]{4}/[0-9]{2}/[0-9]{2} )"
exit "${PIPESTATUS[0]}"
