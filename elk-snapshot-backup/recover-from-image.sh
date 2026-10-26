#!/bin/bash
# 호스트(내 PC) 터미널에서 실행합니다
docker compose down                          # 망가진 서버 제거
docker tag elk-lab:installed elk-lab-vm      # 스냅샷을 현재 이미지로 지정
docker compose up -d --no-build              # 다시 빌드하지 않고 기동
