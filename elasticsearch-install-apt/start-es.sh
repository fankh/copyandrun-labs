#!/bin/bash
sudo -u elasticsearch env ES_PATH_CONF=/etc/elasticsearch \
  /usr/share/elasticsearch/bin/elasticsearch -d -p /tmp/es.pid > /dev/null 2>&1

# 기동될 때까지 기다립니다(1~2분)
until curl -sf -o /dev/null http://127.0.0.1:9200/_cluster/health; do sleep 3; done
echo "기동 완료"

curl -s "http://127.0.0.1:9200/_cluster/health?pretty" | head -6
curl -s http://127.0.0.1:9200 | head -8      # 버전 확인
