#!/bin/sh
# 연습용 PostgreSQL 16 을 띄웁니다. 키 노출 위험을 눈으로 보려고 log_statement=all 로 시작합니다.
docker volume create cr-p22-data >/dev/null
docker run -d --name cr-p22-db \
  -e POSTGRES_PASSWORD=lab-admin-pw \
  -p 127.0.0.1:18170:5432 \
  -v cr-p22-data:/var/lib/postgresql/data \
  postgres:16 \
  -c log_statement=all \
  -c shared_preload_libraries=pg_stat_statements
until docker exec cr-p22-db pg_isready -U postgres >/dev/null 2>&1; do sleep 1; done
sleep 2
docker exec cr-p22-db psql -U postgres -Atc "select version()" | cut -c1-40
