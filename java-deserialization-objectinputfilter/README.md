# Java 역직렬화 위험과 ObjectInputFilter: 허용한 클래스만 읽게 제한하기

직접 만든 연습용 클래스 Dangerous 의 readObject 가 필터 없이 실행되는 것을 확인하고, ObjectInputFilter 패턴 com.example.Safe;!* 로 거절되는 것을 비교합니다. maxdepth, maxarray, maxbytes 한도와 jdk.serialFilter 전역 설정, 허용 목록에서 자주 놓치는 클래스도 JDK 21 컨테이너에서 실행해 봅니다.

글: https://copyandrun.com/blog/java-deserialization-objectinputfilter/

## 파일

- `App.java`
- `Blob.java`
- `Dangerous.java`
- `Node.java`
- `Safe.java`

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
