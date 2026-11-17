#!/bin/sh
# 공식 misp-docker 구성을 내려받아 연습용 값으로 .env 를 만듭니다.
# 아래 비밀번호와 API 키는 이 연습용 서버에서만 쓰는 값이며 실제 서버에 쓰지 않습니다.
ADMIN_ID=admin
ADMIN_HOST=example.com
BASE=https://raw.githubusercontent.com/MISP/misp-docker/master
curl -sL $BASE/docker-compose.yml -o docker-compose.yml
curl -sL $BASE/template.env -o .env
sed -i \
  -e "s|^ADMIN_EMAIL=.*|ADMIN_EMAIL=$ADMIN_ID@$ADMIN_HOST|" \
  -e 's|^ADMIN_ORG=.*|ADMIN_ORG=LabOrg|' \
  -e 's|^ADMIN_KEY=.*|ADMIN_KEY=CrC11LabKeyTestOnly0123456789abcdefghijk|' \
  -e 's|^ADMIN_PASSWORD=.*|ADMIN_PASSWORD=Lab-Misp-Pass-2026|' \
  -e 's|^BASE_URL=.*|BASE_URL=http://localhost:18060|' .env
grep -E '^(CORE_TAG|MODULES_TAG|ADMIN_ORG|BASE_URL)=' .env
