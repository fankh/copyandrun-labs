#!/bin/bash
# OpenSearch ml-commons 에 Ollama 를 원격 모델로 등록하고 배포합니다. tools 컨테이너 안에서 실행합니다.
OS=http://opensearch:9200

curl -s -XPUT $OS/_cluster/settings -H 'Content-Type: application/json' -d '{
  "persistent": {
    "plugins.ml_commons.only_run_on_ml_node": false,
    "plugins.ml_commons.connector.private_ip_enabled": true,
    "plugins.ml_commons.trusted_connector_endpoints_regex": ["^http://ollama:11434/.*$"]
  }
}'
echo

CONNECTOR_ID=$(curl -s -XPOST $OS/_plugins/_ml/connectors/_create -H 'Content-Type: application/json' -d '{
  "name": "Ollama Chat",
  "version": "1",
  "protocol": "http",
  "credential": { "key": "ollama-no-auth" },
  "parameters": { "endpoint": "ollama:11434", "model": "qwen2.5:3b" },
  "actions": [{
    "action_type": "predict",
    "method": "POST",
    "url": "http://${parameters.endpoint}/v1/chat/completions",
    "headers": { "Content-Type": "application/json" },
    "request_body": "{ \"model\": \"${parameters.model}\", \"messages\": ${parameters.messages}, \"temperature\": 0 }"
  }]
}' | jq -r .connector_id)

MODEL_ID=$(curl -s -XPOST $OS/_plugins/_ml/models/_register -H 'Content-Type: application/json' \
  -d "{\"name\":\"ollama-chat\",\"function_name\":\"remote\",\"connector_id\":\"$CONNECTOR_ID\"}" | jq -r .model_id)
echo "$MODEL_ID" > /work/model_id.txt

curl -s -XPOST $OS/_plugins/_ml/models/$MODEL_ID/_deploy; echo
sleep 5
curl -s $OS/_plugins/_ml/models/$MODEL_ID | jq -r .model_state
