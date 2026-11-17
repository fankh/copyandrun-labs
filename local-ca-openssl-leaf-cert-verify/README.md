# 내 CA로 서버 인증서 발급하고 openssl verify 검증

OpenSSL 3.5.9로 루트 CA와 서버 인증서를 만들고, 정상 인증서와 이름 불일치, 만료, 용도 불일치, 신뢰하지 않는 CA 서명, SAN 없는 인증서를 openssl verify로 판정합니다. SAN이 없어도 통과하는 점은 자체 규칙으로 막고, nginx에 올려 s_client로 실제 연결 결과까지 대조합니다.

## 링크

- 글: [https://copyandrun.com/blog/local-ca-openssl-leaf-cert-verify/](https://copyandrun.com/blog/local-ca-openssl-leaf-cert-verify/)
- 한 번에 받기: [local-ca-openssl-leaf-cert-verify.zip](https://copyandrun.com/code-zip/local-ca-openssl-leaf-cert-verify.zip)
- GitHub 폴더: [copyandrun-labs/local-ca-openssl-leaf-cert-verify](https://github.com/fankh/copyandrun-labs/tree/main/local-ca-openssl-leaf-cert-verify)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `ca_demo.sh` | <a href="https://fankh.github.io/copyandrun-labs/local-ca-openssl-leaf-cert-verify/ca_demo.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/local-ca-openssl-leaf-cert-verify/ca_demo.sh) |
| `ca_lab.sh` | <a href="https://fankh.github.io/copyandrun-labs/local-ca-openssl-leaf-cert-verify/ca_lab.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/local-ca-openssl-leaf-cert-verify/ca_lab.sh) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
