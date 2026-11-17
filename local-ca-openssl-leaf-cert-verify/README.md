# 내 CA로 서버 인증서 발급하고 openssl verify 검증

OpenSSL 3.5.9로 루트 CA와 서버 인증서를 만들고, 정상 인증서와 이름 불일치, 만료, 용도 불일치, 신뢰하지 않는 CA 서명, SAN 없는 인증서를 openssl verify로 판정합니다. SAN이 없어도 통과하는 점은 자체 규칙으로 막고, nginx에 올려 s_client로 실제 연결 결과까지 대조합니다.

글: https://copyandrun.com/blog/local-ca-openssl-leaf-cert-verify/

## 파일

- `ca_demo.sh`
- `ca_lab.sh`

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
