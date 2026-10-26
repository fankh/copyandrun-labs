#!/bin/bash
# 명령 실행, 파일, 코드 실행, 브라우저, 하위 에이전트, 예약 작업, 외부 연결 도구를 끕니다.
# 남는 것은 MCP filesystem 의 읽기 도구와 기본 도구 몇 개입니다. 컨테이너 안에서 실행합니다.
set -e
hermes tools disable terminal file code_execution browser delegation cronjob connections
hermes tools list | grep -E "terminal|file|code_execution|browser|delegation|cronjob|connections|filesystem"
