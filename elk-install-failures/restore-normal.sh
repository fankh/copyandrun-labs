#!/bin/bash
kill $(cat /tmp/es.pid)
until ! curl -sf -o /dev/null http://127.0.0.1:9200; do sleep 2; done

sudo -u elasticsearch env ES_PATH_CONF=/etc/elasticsearch \
  /usr/share/elasticsearch/bin/elasticsearch -d -p /tmp/es.pid > /dev/null 2>&1
until curl -sf -o /dev/null "http://127.0.0.1:9200/_cluster/health?wait_for_status=yellow&timeout=30s"; do sleep 3; done
curl -s "http://127.0.0.1:9200/_cat/indices/logs-*?h=index,docs.count&s=index"
