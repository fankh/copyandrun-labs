#!/bin/bash
# 서버를 다시 켠 뒤 ES와 Kibana를 올립니다(서버 안에서 root로 실행)
sudo -u elasticsearch env ES_PATH_CONF=/etc/elasticsearch \
  /usr/share/elasticsearch/bin/elasticsearch -d -p /tmp/es.pid > /dev/null 2>&1
sudo -u kibana env KBN_PATH_CONF=/etc/kibana \
  nohup /usr/share/kibana/bin/kibana > /tmp/kibana-start.log 2>&1 &
until curl -sf -o /dev/null http://127.0.0.1:9200/_cluster/health; do sleep 3; done
curl -s "http://127.0.0.1:9200/_cluster/health?wait_for_status=yellow&timeout=60s&pretty" | head -3
