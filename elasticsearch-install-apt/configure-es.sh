#!/bin/bash
# 1) 자동 보안 구성 블록 삭제
sed -i '/BEGIN SECURITY AUTO CONFIGURATION/,/END SECURITY AUTO CONFIGURATION/d' \
  /etc/elasticsearch/elasticsearch.yml

# 2) 실습 설정 추가
cat >> /etc/elasticsearch/elasticsearch.yml <<'CONF'

# ===== 실습 설정 (교육 전용) =====
cluster.name: elk-lab
node.name: elk-vm
discovery.type: single-node
http.host: 0.0.0.0
transport.host: 127.0.0.1
path.repo: /var/lib/elasticsearch/snapshots
xpack.security.enabled: false
xpack.security.enrollment.enabled: false
xpack.security.http.ssl.enabled: false
xpack.security.transport.ssl.enabled: false
CONF

# 3) 스냅샷 저장소로 쓸 폴더를 만들고 소유자를 맞춥니다
mkdir -p /var/lib/elasticsearch/snapshots
chown elasticsearch:elasticsearch /var/lib/elasticsearch/snapshots

# 4) JVM 힙을 1GB로 고정합니다 (최소=최대)
printf -- "-Xms1g\n-Xmx1g\n" > /etc/elasticsearch/jvm.options.d/heap.options
