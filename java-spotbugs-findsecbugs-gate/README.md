# SpotBugs와 Find Security Bugs로 Java 보안 점검 게이트 만들기

Maven 컨테이너에서 SpotBugs 플러그인에 Find Security Bugs를 붙여 SQL 문자열 결합, MD5, 하드코딩 비밀번호, 경로 조작이 심어진 연습용 코드를 점검합니다. XML과 HTML 보고서를 읽고, 코드를 고쳐 결과를 0건으로 만들고, threshold 설정과 이유를 남기는 제외 필터까지 mvn verify 빌드 게이트로 묶습니다.

글: https://copyandrun.com/blog/java-spotbugs-findsecbugs-gate/

## 파일

- `BadgeColor.java`
- `empty-filter.xml`
- `FileService.fixed.java`
- `FileService.java`
- `PasswordUtil.fixed.java`
- `PasswordUtil.java`
- `pom.xml`
- `spotbugs-exclude.xml`
- `summary.sh`
- `UserRepo.fixed.java`
- `UserRepo.java`

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
