# Log4Shell 해부: log4j 2.14.1과 2.17.1의 조회 해석 비교

CVE-2021-44228이 생긴 원리를 로그인 화면이 있는 시험 앱과 무해한 java:version 조회로 재현합니다. 같은 입력을 log4j 2.14.1과 2.17.1에서 브라우저로 넣어 서버 로그를 비교하고, 임시 완화 옵션과 접속 로그 점검 명령까지 정리합니다.

## 링크

- 글: [https://copyandrun.com/blog/log4shell-anatomy-lookup-demo/](https://copyandrun.com/blog/log4shell-anatomy-lookup-demo/)
- 한 번에 받기: [log4shell-anatomy-lookup-demo.zip](https://copyandrun.com/code-zip/log4shell-anatomy-lookup-demo.zip)
- GitHub 폴더: [copyandrun-labs/log4shell-anatomy-lookup-demo](https://github.com/fankh/copyandrun-labs/tree/main/log4shell-anatomy-lookup-demo)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `log4j2.xml` | <a href="https://fankh.github.io/copyandrun-labs/log4shell-anatomy-lookup-demo/log4j2.xml" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/log4shell-anatomy-lookup-demo/log4j2.xml) |
| `pom.xml` | <a href="https://fankh.github.io/copyandrun-labs/log4shell-anatomy-lookup-demo/pom.xml" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/log4shell-anatomy-lookup-demo/pom.xml) |
| `run-web.sh` | <a href="https://fankh.github.io/copyandrun-labs/log4shell-anatomy-lookup-demo/run-web.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/log4shell-anatomy-lookup-demo/run-web.sh) |
| `WebApp.java` | <a href="https://fankh.github.io/copyandrun-labs/log4shell-anatomy-lookup-demo/WebApp.java" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/log4shell-anatomy-lookup-demo/WebApp.java) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
