#!/bin/sh
# 공개 EVTX 샘플 한 개를 고정된 커밋 주소에서 data/ 로 내려받고 SHA-256 을 출력합니다.
# 로그 파일(.evtx)만 받으며 실행 파일은 받지 않습니다. 저장소 라이선스는 GPL-3.0 입니다.
COMMIT=4ceed2f4706daf601c212a8f91c113dd85349a2c
NAME=sideloading_uacbypass_rundll32_injection_c2.evtx
mkdir -p data
curl -fsSL -o "data/$NAME" \
  "https://raw.githubusercontent.com/sbousseaden/EVTX-ATTACK-SAMPLES/$COMMIT/AutomatedTestingTools/Malware/$NAME"
echo "$(wc -c < "data/$NAME") bytes  data/$NAME"
sha256sum "data/$NAME"
