# Ubuntu에서 Elasticsearch 설치하고 기동하기

Elastic 공식 저장소 서명 키 등록부터 apt 설치, 설정 파일 수정, JVM 힙 고정, 클러스터 상태 확인을 차례로 진행합니다.

## 링크

- 글: [https://copyandrun.com/blog/elasticsearch-install-apt/](https://copyandrun.com/blog/elasticsearch-install-apt/)
- 한 번에 받기: [elasticsearch-install-apt.zip](https://copyandrun.com/code-zip/elasticsearch-install-apt.zip)
- GitHub 폴더: [copyandrun-labs/elasticsearch-install-apt](https://github.com/fankh/copyandrun-labs/tree/main/elasticsearch-install-apt)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `add-elastic-repo.sh` | <a href="https://fankh.github.io/copyandrun-labs/elasticsearch-install-apt/add-elastic-repo.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/elasticsearch-install-apt/add-elastic-repo.sh) |
| `configure-es.sh` | <a href="https://fankh.github.io/copyandrun-labs/elasticsearch-install-apt/configure-es.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/elasticsearch-install-apt/configure-es.sh) |
| `start-es.sh` | <a href="https://fankh.github.io/copyandrun-labs/elasticsearch-install-apt/start-es.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/elasticsearch-install-apt/start-es.sh) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
