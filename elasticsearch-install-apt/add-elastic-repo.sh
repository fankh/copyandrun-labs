#!/bin/bash
# 1) 패키지 서명 검증용 공개키를 내려받아 키링에 넣습니다
curl -fsSL https://artifacts.elastic.co/GPG-KEY-elasticsearch \
  | gpg --dearmor -o /usr/share/keyrings/elastic-keyring.gpg

# 2) 저장소 주소를 등록합니다 (signed-by 로 위 키를 지정 - 서명이 맞아야만 설치됩니다)
KEY=/usr/share/keyrings/elastic-keyring.gpg
REPO=https://artifacts.elastic.co/packages/8.x/apt
LIST=/etc/apt/sources.list.d/elastic-8.x.list
printf 'deb [signed-by=%s] %s stable main\n' "$KEY" "$REPO" > "$LIST"

# 등록 내용이 "한 줄"인지 반드시 확인합니다
cat "$LIST"

# 3) 패키지 목록 갱신 후 설치 가능한 버전을 봅니다
apt-get update
apt-cache madison elasticsearch | head -3
