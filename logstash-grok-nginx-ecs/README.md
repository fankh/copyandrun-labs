# Logstash로 nginx 로그를 Grok으로 파싱하고 ECS로 정규화하기

nginx 접근 로그를 Logstash grok으로 파싱해 ECS 필드 이름으로 정리하고, 파싱에 실패한 로그를 Elasticsearch 쿼리로 세어 별도 인덱스로 보냅니다. Docker로 Elasticsearch 8.19와 Logstash 8.19를 띄워 끝까지 돌리고, Kibana Discover에서 적재된 필드를 확인합니다.

## 링크

- 글: [https://copyandrun.com/blog/logstash-grok-nginx-ecs/](https://copyandrun.com/blog/logstash-grok-nginx-ecs/)
- 한 번에 받기: [logstash-grok-nginx-ecs.zip](https://copyandrun.com/code-zip/logstash-grok-nginx-ecs.zip)
- GitHub 폴더: [copyandrun-labs/logstash-grok-nginx-ecs](https://github.com/fankh/copyandrun-labs/tree/main/logstash-grok-nginx-ecs)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `access.log` | <a href="https://fankh.github.io/copyandrun-labs/logstash-grok-nginx-ecs/access.log" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/logstash-grok-nginx-ecs/access.log) |
| `compose.yml` | <a href="https://fankh.github.io/copyandrun-labs/logstash-grok-nginx-ecs/compose.yml" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/logstash-grok-nginx-ecs/compose.yml) |
| `kibana-setup.sh` | <a href="https://fankh.github.io/copyandrun-labs/logstash-grok-nginx-ecs/kibana-setup.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/logstash-grok-nginx-ecs/kibana-setup.sh) |
| `pipeline-2-stdin.conf` | <a href="https://fankh.github.io/copyandrun-labs/logstash-grok-nginx-ecs/pipeline-2-stdin.conf" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/logstash-grok-nginx-ecs/pipeline-2-stdin.conf) |
| `pipeline-3-custom.conf` | <a href="https://fankh.github.io/copyandrun-labs/logstash-grok-nginx-ecs/pipeline-3-custom.conf" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/logstash-grok-nginx-ecs/pipeline-3-custom.conf) |
| `pipeline-4-file-to-es.conf` | <a href="https://fankh.github.io/copyandrun-labs/logstash-grok-nginx-ecs/pipeline-4-file-to-es.conf" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/logstash-grok-nginx-ecs/pipeline-4-file-to-es.conf) |
| `pipeline-5-split.conf` | <a href="https://fankh.github.io/copyandrun-labs/logstash-grok-nginx-ecs/pipeline-5-split.conf" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/logstash-grok-nginx-ecs/pipeline-5-split.conf) |
| `run.sh` | <a href="https://fankh.github.io/copyandrun-labs/logstash-grok-nginx-ecs/run.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/logstash-grok-nginx-ecs/run.sh) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
