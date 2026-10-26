#!/bin/bash
# 서버 안에서 실행합니다. 이미지로 복구한 뒤 ES가 뜨지 않을 때 쓰는 복구 절차
curl -s -o /dev/null -w 'ES HTTP: %{http_code}\n' http://127.0.0.1:9200
grep AlreadyClosedException /var/log/elasticsearch/elk-lab.log | tail -1 | cut -c1-110

# 파일 수정 시각을 현재로 갱신해 "외부에서 바뀐 파일"이라는 판정을 없앱니다
find /var/lib/elasticsearch -type f -exec touch {} +

sudo -u elasticsearch env ES_PATH_CONF=/etc/elasticsearch \
  /usr/share/elasticsearch/bin/elasticsearch -d -p /tmp/es.pid > /dev/null 2>&1
until curl -sf -o /dev/null http://127.0.0.1:9200/_cluster/health; do sleep 3; done
echo "ES 기동 완료"
curl -s "http://127.0.0.1:9200/_cat/indices/logs-*?h=index,docs.count&s=index"
curl -s "http://127.0.0.1:9200/_cat/snapshots/backup?h=id,status"
