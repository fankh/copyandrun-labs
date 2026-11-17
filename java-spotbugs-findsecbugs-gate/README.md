# SpotBugs와 Find Security Bugs로 Java 보안 점검 게이트 만들기

Maven 컨테이너에서 SpotBugs 플러그인에 Find Security Bugs를 붙여 SQL 문자열 결합, MD5, 하드코딩 비밀번호, 경로 조작이 심어진 연습용 코드를 점검합니다. XML과 HTML 보고서를 읽고, 코드를 고쳐 결과를 0건으로 만들고, threshold 설정과 이유를 남기는 제외 필터까지 mvn verify 빌드 게이트로 묶습니다.

## 링크

- 글: [https://copyandrun.com/blog/java-spotbugs-findsecbugs-gate/](https://copyandrun.com/blog/java-spotbugs-findsecbugs-gate/)
- 한 번에 받기: [java-spotbugs-findsecbugs-gate.zip](https://copyandrun.com/code-zip/java-spotbugs-findsecbugs-gate.zip)
- GitHub 폴더: [copyandrun-labs/java-spotbugs-findsecbugs-gate](https://github.com/fankh/copyandrun-labs/tree/main/java-spotbugs-findsecbugs-gate)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `BadgeColor.java` | <a href="https://fankh.github.io/copyandrun-labs/java-spotbugs-findsecbugs-gate/BadgeColor.java" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/java-spotbugs-findsecbugs-gate/BadgeColor.java) |
| `empty-filter.xml` | <a href="https://fankh.github.io/copyandrun-labs/java-spotbugs-findsecbugs-gate/empty-filter.xml" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/java-spotbugs-findsecbugs-gate/empty-filter.xml) |
| `FileService.fixed.java` | <a href="https://fankh.github.io/copyandrun-labs/java-spotbugs-findsecbugs-gate/FileService.fixed.java" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/java-spotbugs-findsecbugs-gate/FileService.fixed.java) |
| `FileService.java` | <a href="https://fankh.github.io/copyandrun-labs/java-spotbugs-findsecbugs-gate/FileService.java" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/java-spotbugs-findsecbugs-gate/FileService.java) |
| `PasswordUtil.fixed.java` | <a href="https://fankh.github.io/copyandrun-labs/java-spotbugs-findsecbugs-gate/PasswordUtil.fixed.java" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/java-spotbugs-findsecbugs-gate/PasswordUtil.fixed.java) |
| `PasswordUtil.java` | <a href="https://fankh.github.io/copyandrun-labs/java-spotbugs-findsecbugs-gate/PasswordUtil.java" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/java-spotbugs-findsecbugs-gate/PasswordUtil.java) |
| `pom.xml` | <a href="https://fankh.github.io/copyandrun-labs/java-spotbugs-findsecbugs-gate/pom.xml" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/java-spotbugs-findsecbugs-gate/pom.xml) |
| `spotbugs-exclude.xml` | <a href="https://fankh.github.io/copyandrun-labs/java-spotbugs-findsecbugs-gate/spotbugs-exclude.xml" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/java-spotbugs-findsecbugs-gate/spotbugs-exclude.xml) |
| `summary.sh` | <a href="https://fankh.github.io/copyandrun-labs/java-spotbugs-findsecbugs-gate/summary.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/java-spotbugs-findsecbugs-gate/summary.sh) |
| `UserRepo.fixed.java` | <a href="https://fankh.github.io/copyandrun-labs/java-spotbugs-findsecbugs-gate/UserRepo.fixed.java" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/java-spotbugs-findsecbugs-gate/UserRepo.fixed.java) |
| `UserRepo.java` | <a href="https://fankh.github.io/copyandrun-labs/java-spotbugs-findsecbugs-gate/UserRepo.java" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/java-spotbugs-findsecbugs-gate/UserRepo.java) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
