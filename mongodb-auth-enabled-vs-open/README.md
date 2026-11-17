# MongoDB 인증 켜기와 최소 권한 사용자: 열린 서버, 루트 공유, 역할 분리 비교

인증 없이 뜬 MongoDB 8은 같은 네트워크의 다른 컨테이너가 DB 목록을 보고 급여 문서를 읽고 컬렉션을 지울 수 있습니다. 인증을 켠 서버에서 앱이 루트 계정을 그대로 쓰는 경우와 앱용, 보고용 사용자를 나눈 경우를 5가지 동작 20칸 표로 비교하고, connectionStatus와 서버 로그로 교차 확인합니다.

글: https://copyandrun.com/blog/mongodb-auth-enabled-vs-open/

## 파일

- `mongo_demo.sh`
- `mongo_peek.sh`
- `peek.js`
- `plant.js`
- `probe.js`
- `users.js`

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
