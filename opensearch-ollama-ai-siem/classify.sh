#!/bin/bash
# 401 이 가장 많은 IP 를 찾아 LLM 에 분류를 맡깁니다. tools 컨테이너 안에서 실행합니다.
OS=http://opensearch:9200
MODEL_ID=$(cat /work/model_id.txt)

EVENT=$(curl -s $OS/security-web/_search -H 'Content-Type: application/json' -d '{
  "size": 0,
  "query": { "term": { "http.response.status_code": 401 } },
  "aggs": { "by_ip": { "terms": { "field": "source.ip.keyword", "size": 1 } } }
}' | jq -r '.aggregations.by_ip.buckets[0] | "\(.key) 가 /login 에 401 을 \(.doc_count)회 발생, UA=python-requests/2.31"')
echo "$EVENT"

jq -n --arg event "$EVENT" '{parameters: {messages: [
  {role: "system", content: "너는 SOC 분석가다. 한국어 3줄로 답한다. 1)공격유형 2)심각도(상/중/하) 3)권고. 공격유형은 [브루트포스,SQLi,XSS,스캐닝,정상] 중 하나. 신호: /login 401 다수=브루트포스, UNION SELECT나 UA=sqlmap=SQLi, <script>=XSS, 경로 404 다수=스캐닝, 2xx 정상응답만=정상."},
  {role: "user", content: "10.20.30.40 가 2분간 /login 에 POST 200건, 대부분 401, UA=hydra."},
  {role: "assistant", content: "공격유형: 브루트포스\n심각도: 상\n권고: 해당 IP 차단 + 로그인 rate limit."},
  {role: "user", content: "192.168.10.5 가 /index.html, /a.css GET 12건 모두 200."},
  {role: "assistant", content: "공격유형: 정상\n심각도: 하\n권고: 조치 불필요."},
  {role: "user", content: $event}]}}' > /work/predict_body.json

curl -s -XPOST $OS/_plugins/_ml/models/$MODEL_ID/_predict -H 'Content-Type: application/json' -d @/work/predict_body.json \
  | jq -r '.inference_results[0].output[0].dataAsMap.choices[0].message.content'
