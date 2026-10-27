#!/bin/bash
# Open WebUI 가 실제로 쓰는 Ollama 주소와 보이는 모델 수를 확인합니다.
# 사용법: ./check-ollama.sh [새 Ollama 주소]   (주소를 주면 그 값으로 바꿉니다)
BASE=http://localhost:5600
USER_ID=lab
MAIL_HOST=lab.test
EMAIL="$USER_ID@$MAIL_HOST"
PASS=lab-only-pass-123

TOKEN=$(curl -s -X POST $BASE/api/v1/auths/signin -H 'content-type: application/json' \
  -d "{\"email\":\"$EMAIL\",\"password\":\"$PASS\"}" | python -c "import sys,json;print(json.load(sys.stdin)['token'])")

if [ -n "$1" ]; then
  curl -s -X POST $BASE/ollama/config/update -H "Authorization: Bearer $TOKEN" \
    -H 'content-type: application/json' \
    -d "{\"ENABLE_OLLAMA_API\":true,\"OLLAMA_BASE_URLS\":[\"$1\"],\"OLLAMA_API_CONFIGS\":{}}" > /dev/null
fi

echo "container env : $(docker exec cr-open-webui printenv OLLAMA_BASE_URL)"
echo "saved setting : $(curl -s $BASE/ollama/config -H "Authorization: Bearer $TOKEN" | python -c "import sys,json;print(json.load(sys.stdin)['OLLAMA_BASE_URLS'][0])")"
echo "models seen   : $(curl -s $BASE/api/models -H "Authorization: Bearer $TOKEN" | python -c "import sys,json;print(len(json.load(sys.stdin)['data']))")"
