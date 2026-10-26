# Ubuntu에서 Elasticsearch 설치하고 기동하기

Elastic 공식 저장소 서명 키 등록부터 apt 설치, 설정 파일 수정, JVM 힙 고정, 클러스터 상태 확인을 차례로 진행합니다.

글: https://copyandrun.com/blog/elasticsearch-install-apt/

## 파일

- `add-elastic-repo.sh`
- `configure-es.sh`
- `start-es.sh`

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
