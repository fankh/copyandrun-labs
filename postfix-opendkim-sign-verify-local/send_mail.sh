#!/bin/sh
# 보내는 서버에서 메일 1통을 보냅니다. 주소는 이름과 도메인을 나눠 조립합니다.
DOM=example.internal
docker exec -i cr-fx-send sendmail -t -f "alice@$DOM" <<MAIL
From: Alice <alice@$DOM>
To: carol@$DOM
Subject: DKIM test mail
Date: Mon, 02 Nov 2026 09:00:00 +0900
Message-ID: <dkim-test-1@$DOM>

Report total 100 units.
Line two of the body.
MAIL
