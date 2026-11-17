# HashiCorp Vault 개발 서버: KV 버전, 읽기 전용 정책

Vault 개발 서버를 컨테이너로 띄워 KV 저장과 버전, 읽기 전용 정책, 20초짜리 토큰의 만료, 감사 로그에서 값이 해시로 가려지는 것, 재시작하면 데이터가 사라지는 것까지 실행해 확인합니다.

## 링크

- 글: [https://copyandrun.com/blog/vault-dev-mode-kv-policy/](https://copyandrun.com/blog/vault-dev-mode-kv-policy/)
- 한 번에 받기: [vault-dev-mode-kv-policy.zip](https://copyandrun.com/code-zip/vault-dev-mode-kv-policy.zip)
- GitHub 폴더: [copyandrun-labs/vault-dev-mode-kv-policy](https://github.com/fankh/copyandrun-labs/tree/main/vault-dev-mode-kv-policy)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `app-read.hcl` | <a href="https://fankh.github.io/copyandrun-labs/vault-dev-mode-kv-policy/app-read.hcl" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/vault-dev-mode-kv-policy/app-read.hcl) |
| `vault_demo.sh` | <a href="https://fankh.github.io/copyandrun-labs/vault-dev-mode-kv-policy/vault_demo.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/vault-dev-mode-kv-policy/vault_demo.sh) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
