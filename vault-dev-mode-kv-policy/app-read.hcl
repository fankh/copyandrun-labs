# secret/app/ 아래는 읽기와 목록만 허용한다(KV v2 는 data/ 와 metadata/ 경로를 쓴다)
path "secret/data/app/*" {
  capabilities = ["read"]
}
path "secret/metadata/app/*" {
  capabilities = ["list", "read"]
}
