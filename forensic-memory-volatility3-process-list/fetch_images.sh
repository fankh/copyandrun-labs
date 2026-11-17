#!/bin/sh
# Digital Corpora M57-Patents 시나리오의 RAM 이미지 두 개를 ./images 에 내려받고 SHA-256 을 확인합니다.
set -e
BASE=https://digitalcorpora.s3.amazonaws.com/corpora/scenarios/2009-m57-patents/ram
mkdir -p images
cd images
while read -r name sum; do
  [ -f "$name" ] || curl -sSfLO "$BASE/$name"
  echo "$sum  $name" | sha256sum -c -
  [ -f "${name%.zip}" ] || unzip -q "$name"
done <<'LIST'
pat-2009-12-05.winddramimage.zip 797d24a4025b52465aa1d332019355e5bcb7c7fda55f6b30c4085d6b36f10e78
pat-2009-11-17.mddramimage.zip 7dd6e4e0f7f813f8414eca3fa0f7d6f708dca36c47db76664af27783a312226b
LIST
sha256sum pat-2009-12-05.winddramimage pat-2009-11-17.mddramimage
