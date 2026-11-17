# nginx 보안 헤더 설정 전후 비교: add_header가 404와 일부 경로에서 빠지는 함정

보안 헤더가 없는 nginx, 헤더를 server에만 둔 nginx, 올바르게 설정한 nginx를 만들어 네 경로의 응답 헤더를 스크립트로 검사합니다. 같은 설정인데 로그인과 API 경로와 404 응답에서 헤더가 빠지는 것을 확인하고, 서버 버전 노출과 쿠키 속성까지 종료 코드 게이트로 묶습니다.

## 링크

- 글: [https://copyandrun.com/blog/security-headers-nginx-before-after/](https://copyandrun.com/blog/security-headers-nginx-before-after/)
- 한 번에 받기: [security-headers-nginx-before-after.zip](https://copyandrun.com/code-zip/security-headers-nginx-before-after.zip)
- GitHub 폴더: [copyandrun-labs/security-headers-nginx-before-after](https://github.com/fankh/copyandrun-labs/tree/main/security-headers-nginx-before-after)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `bad.conf` | <a href="https://fankh.github.io/copyandrun-labs/security-headers-nginx-before-after/bad.conf" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/security-headers-nginx-before-after/bad.conf) |
| `good.conf` | <a href="https://fankh.github.io/copyandrun-labs/security-headers-nginx-before-after/good.conf" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/security-headers-nginx-before-after/good.conf) |
| `hdr_audit.py` | <a href="https://fankh.github.io/copyandrun-labs/security-headers-nginx-before-after/hdr_audit.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/security-headers-nginx-before-after/hdr_audit.py) |
| `headers_demo.sh` | <a href="https://fankh.github.io/copyandrun-labs/security-headers-nginx-before-after/headers_demo.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/security-headers-nginx-before-after/headers_demo.sh) |
| `naive.conf` | <a href="https://fankh.github.io/copyandrun-labs/security-headers-nginx-before-after/naive.conf" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/security-headers-nginx-before-after/naive.conf) |
| `snippet_headers.conf` | <a href="https://fankh.github.io/copyandrun-labs/security-headers-nginx-before-after/snippet_headers.conf" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/security-headers-nginx-before-after/snippet_headers.conf) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
