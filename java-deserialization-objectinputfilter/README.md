# Java 역직렬화 위험과 ObjectInputFilter: 허용한 클래스만 읽게 제한하기

직접 만든 연습용 클래스 Dangerous 의 readObject 가 필터 없이 실행되는 것을 확인하고, ObjectInputFilter 패턴 com.example.Safe;!* 로 거절되는 것을 비교합니다. maxdepth, maxarray, maxbytes 한도와 jdk.serialFilter 전역 설정, 허용 목록에서 자주 놓치는 클래스도 JDK 21 컨테이너에서 실행해 봅니다.

## 링크

- 글: [https://copyandrun.com/blog/java-deserialization-objectinputfilter/](https://copyandrun.com/blog/java-deserialization-objectinputfilter/)
- 한 번에 받기: [java-deserialization-objectinputfilter.zip](https://copyandrun.com/code-zip/java-deserialization-objectinputfilter.zip)
- GitHub 폴더: [copyandrun-labs/java-deserialization-objectinputfilter](https://github.com/fankh/copyandrun-labs/tree/main/java-deserialization-objectinputfilter)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `App.java` | <a href="https://fankh.github.io/copyandrun-labs/java-deserialization-objectinputfilter/App.java" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/java-deserialization-objectinputfilter/App.java) |
| `Blob.java` | <a href="https://fankh.github.io/copyandrun-labs/java-deserialization-objectinputfilter/Blob.java" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/java-deserialization-objectinputfilter/Blob.java) |
| `Dangerous.java` | <a href="https://fankh.github.io/copyandrun-labs/java-deserialization-objectinputfilter/Dangerous.java" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/java-deserialization-objectinputfilter/Dangerous.java) |
| `Node.java` | <a href="https://fankh.github.io/copyandrun-labs/java-deserialization-objectinputfilter/Node.java" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/java-deserialization-objectinputfilter/Node.java) |
| `Safe.java` | <a href="https://fankh.github.io/copyandrun-labs/java-deserialization-objectinputfilter/Safe.java" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/java-deserialization-objectinputfilter/Safe.java) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
