# Logstash로 nginx 로그를 Grok으로 파싱하고 ECS로 정규화하기

nginx 접근 로그를 Logstash grok으로 파싱해 ECS 필드 이름으로 정리하고, 파싱에 실패한 로그를 Elasticsearch 쿼리로 세어 별도 인덱스로 보냅니다. Docker로 Elasticsearch 8.19와 Logstash 8.19를 띄워 끝까지 돌리고, Kibana Discover에서 적재된 필드를 확인합니다.

글: https://copyandrun.com/blog/logstash-grok-nginx-ecs/

## 파일

- `access.log`
- `compose.yml`
- `kibana-setup.sh`
- `pipeline-2-stdin.conf`
- `pipeline-3-custom.conf`
- `pipeline-4-file-to-es.conf`
- `pipeline-5-split.conf`
- `run.sh`

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
