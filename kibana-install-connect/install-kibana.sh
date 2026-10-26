#!/bin/bash
apt-get install -y kibana

cat >> /etc/kibana/kibana.yml <<'CONF'

# ===== 실습 설정 (교육 전용) =====
server.host: "0.0.0.0"
server.publicBaseUrl: "http://127.0.0.1:5601"
elasticsearch.hosts: ["http://localhost:9200"]
CONF

mkdir -p /var/log/kibana
chown -R kibana:kibana /var/log/kibana

sudo -u kibana env KBN_PATH_CONF=/etc/kibana \
  nohup /usr/share/kibana/bin/kibana > /tmp/kibana-start.log 2>&1 &

# Kibana는 기동이 느립니다(1~3분)
until curl -sf -o /dev/null http://127.0.0.1:5601/api/status; do sleep 5; done
echo "Kibana 기동 완료"
