#!/usr/bin/env bash
# HashiCorp Vault 개발 서버로 KV 저장, 버전, 읽기 전용 정책, 토큰 만료, 감사 로그를 확인한다.
# 준비: Docker, 같은 폴더에 app-read.hcl. 개발 서버는 메모리에만 저장하고 root 토큰이 고정이므로 내 PC 시험 전용이다.
# 실행(Git Bash): bash vault_demo.sh   (약 1분)
export MSYS_NO_PATHCONV=1
HERE="$(pwd)"
ROOT=root-lab-token
V()  { docker exec -e VAULT_ADDR=http://127.0.0.1:8200 -e VAULT_TOKEN="$ROOT" osk-vault vault "$@"; }
VT() { local t="$1"; shift; docker exec -e VAULT_ADDR=http://127.0.0.1:8200 -e VAULT_TOKEN="$t" osk-vault vault "$@"; }
start() {
  docker rm -f osk-vault >/dev/null 2>&1
  docker run -d --name osk-vault --cap-add IPC_LOCK -e VAULT_DEV_ROOT_TOKEN_ID=$ROOT \
    -e VAULT_DEV_LISTEN_ADDRESS=0.0.0.0:8200 hashicorp/vault:latest >/dev/null
  sleep 4
}
start

echo "## 1. 개발 서버 상태(메모리 저장, 자동 unseal)"
V version | cut -c1-14
V status | grep -E 'Initialized|Sealed|Storage|Version'

echo "## 2. KV v2: 저장, 덮어쓰기(버전 증가), 옛 버전 읽기"
V kv put -mount=secret app/db user=app pass=first >/dev/null
V kv put -mount=secret app/db user=app pass=second | grep -E '^version'
echo -n "  현재 값:    "; V kv get -mount=secret -field=pass app/db; echo
echo -n "  1번 버전:   "; V kv get -mount=secret -version=1 -field=pass app/db; echo
V kv delete -mount=secret app/db >/dev/null
echo -n "  삭제 뒤:    값 줄 수 "; V kv get -mount=secret app/db 2>&1 | grep -c '^pass'; V kv get -mount=secret app/db 2>&1 | grep deletion_time | sed 's/^/              /'
V kv undelete -versions=2 -mount=secret app/db >/dev/null
echo -n "  복구 뒤:    "; V kv get -mount=secret -field=pass app/db; echo

echo "## 3. 읽기 전용 정책과 짧은 수명의 토큰(20초)"
docker exec -i osk-vault sh -c 'cat > /tmp/app-read.hcl' < "$HERE/app-read.hcl"   # docker cp 는 Git Bash 경로에서 실패해서 표준 입력으로 넘긴다
V policy write app-read /tmp/app-read.hcl
V kv put -mount=secret other/key value=hidden >/dev/null
TOK=$(V token create -policy=app-read -ttl=20s -field=token)
echo "  토큰 앞 8자: ${TOK:0:8}..."
echo -n "  읽기 secret/app/db : "; VT "$TOK" kv get -mount=secret -field=pass app/db; echo
echo -n "  쓰기 secret/app/db : "; VT "$TOK" kv put -mount=secret app/db pass=hacked 2>&1 | grep -o 'permission denied' | head -1
echo -n "  읽기 secret/other  : "; VT "$TOK" kv get -mount=secret other/key 2>&1 | grep -o 'permission denied' | head -1
echo -n "  토큰 남은 수명(초) : "; VT "$TOK" token lookup -format=json | python -c "import json,sys; print(json.load(sys.stdin)['data']['ttl'])"

echo "## 4. 20초가 지난 뒤에 같은 토큰으로 읽기"
sleep 22
echo -n "  읽기: "; VT "$TOK" kv get -mount=secret -field=pass app/db 2>&1 | grep -oE 'permission denied|bad token|invalid token' | head -1

echo "## 5. 감사 로그: 켠 뒤의 요청만 남고, 값은 해시로 가려진다"
V audit enable file file_path=/tmp/audit.log >/dev/null
V kv get -mount=secret -field=pass app/db >/dev/null
TOK2=$(V token create -policy=app-read -ttl=60s -field=token)
VT "$TOK2" kv put -mount=secret app/db pass=hacked >/dev/null 2>&1
docker exec osk-vault cat /tmp/audit.log | python -c "
import json, sys
for line in sys.stdin:
    d = json.loads(line)
    r = d.get('request', {})
    if d['type'] == 'request' and r.get('path', '').startswith('secret/data/app'):
        print(f\"  {d['type']:8} {r['operation']:7} {r['path']:20} policies={d.get('auth', {}).get('policies')}\")
" 
echo -n "  로그에 평문 'second' 가 있는가: "; docker exec osk-vault grep -c second /tmp/audit.log
echo -n "  로그에 평문 'hacked' 가 있는가: "; docker exec osk-vault grep -c hacked /tmp/audit.log

echo "## 6. HTTP API 로도 같은 값을 읽는다(wget)"
docker exec osk-vault wget -qO- --header="X-Vault-Token: $ROOT" http://127.0.0.1:8200/v1/secret/data/app/db \
  | python -c "import json,sys; d=json.load(sys.stdin)['data']; print('  version', d['metadata']['version'], 'pass', d['data']['pass'])"

echo "## 7. 개발 서버를 다시 시작하면 데이터가 사라진다"
docker restart osk-vault >/dev/null; sleep 4
echo -n "  재시작 뒤 읽기: "; V kv get -mount=secret app/db 2>&1 | head -1 | cut -c1-70

echo "## 8. 정리"
docker rm -f osk-vault >/dev/null
docker ps -a --format '{{.Names}}' | grep -c osk-vault
