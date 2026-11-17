# Copy & Run 실습 코드

[https://copyandrun.com](https://copyandrun.com) 의 글에서 쓰는 실습 코드 모음입니다. 폴더 이름이 글 주소의 마지막 부분과 같습니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다.

| 폴더 | 글 |
| --- | --- |
| [`account-audit-uid0-empty-password`](account-audit-uid0-empty-password/) | [Linux 계정 점검: UID 0 계정, 빈 암호, 로그인 셸이 있는 시스템 계정을 awk로 찾기](https://copyandrun.com/blog/account-audit-uid0-empty-password/) |
| [`agent-config-hidden-instructions-scan`](agent-config-hidden-instructions-scan/) | [저장소의 에이전트 설정 파일에 숨은 지시 찾아내기](https://copyandrun.com/blog/agent-config-hidden-instructions-scan/) |
| [`ai-generated-login-code-semgrep-review`](ai-generated-login-code-semgrep-review/) | [생성형 AI가 짜 줄 법한 Flask 로그인 코드를 Semgrep으로 점검하기](https://copyandrun.com/blog/ai-generated-login-code-semgrep-review/) |
| [`ai-hallucinated-package-name-check`](ai-hallucinated-package-name-check/) | [AI가 지어낸 패키지 이름 가려내기: 설치 전 PyPI 조회와 CI 게이트](https://copyandrun.com/blog/ai-hallucinated-package-name-check/) |
| [`aide-file-integrity-baseline`](aide-file-integrity-baseline/) | [AIDE로 파일 무결성 기준선 만들고 변경 감지하기: 수정, 권한, 삭제, 추가와 기준선 바꿔치기](https://copyandrun.com/blog/aide-file-integrity-baseline/) |
| [`apache-axis1-cve-2026-90436-check`](apache-axis1-cve-2026-90436-check/) | [CVE-2026-90436 점검: 서버에서 Apache Axis 1.x jar 찾기와 조치](https://copyandrun.com/blog/apache-axis1-cve-2026-90436-check/) |
| [`api-bola-object-level-authz-test`](api-bola-object-level-authz-test/) | [API BOLA 점검: 로그인한 사용자가 남의 주문 번호로 조회되는지 직접 시험하기](https://copyandrun.com/blog/api-bola-object-level-authz-test/) |
| [`api-excessive-data-exposure-response-filter`](api-excessive-data-exposure-response-filter/) | [API 과다 응답 걸러 내기: FastAPI response_model과 응답 필드 점검 게이트](https://copyandrun.com/blog/api-excessive-data-exposure-response-filter/) |
| [`api-mass-assignment-pydantic-allowlist`](api-mass-assignment-pydantic-allowlist/) | [API 대량 할당 막기: FastAPI Pydantic extra=forbid](https://copyandrun.com/blog/api-mass-assignment-pydantic-allowlist/) |
| [`attack-navigator-sigma-coverage-map`](attack-navigator-sigma-coverage-map/) | [ATT&CK Navigator로 Sigma 탐지 규칙 범위 그리기](https://copyandrun.com/blog/attack-navigator-sigma-coverage-map/) |
| [`caddy-reverse-proxy-basic-auth-https`](caddy-reverse-proxy-basic-auth-https/) | [Caddy 리버스 프록시에 HTTPS와 기본 인증 걸기](https://copyandrun.com/blog/caddy-reverse-proxy-basic-auth-https/) |
| [`capa-rule-match-capabilities`](capa-rule-match-capabilities/) | [capa로 실행 파일의 기능 규칙 맞춰 보기: 어떤 동작을 근거로 판단하는지](https://copyandrun.com/blog/capa-rule-match-capabilities/) |
| [`checkov-terraform-misconfig`](checkov-terraform-misconfig/) | [Checkov로 Terraform 설정 오류를 찾고 고치기](https://copyandrun.com/blog/checkov-terraform-misconfig/) |
| [`ci-semgrep-bandit-gate`](ci-semgrep-bandit-gate/) | [CI에 Semgrep과 Bandit 보안 게이트 붙이기](https://copyandrun.com/blog/ci-semgrep-bandit-gate/) |
| [`conftest-rego-compose-policy`](conftest-rego-compose-policy/) | [conftest와 Rego로 docker-compose 정책 만들기](https://copyandrun.com/blog/conftest-rego-compose-policy/) |
| [`cosign-image-signing-local-registry`](cosign-image-signing-local-registry/) | [컨테이너 이미지에 서명하고 서명 없는 이미지 거부하기(cosign)](https://copyandrun.com/blog/cosign-image-signing-local-registry/) |
| [`dirty-pipe-kernel-version-range-check`](dirty-pipe-kernel-version-range-check/) | [Dirty Pipe 점검: 커널 버전이 CVE-2022-0847 영향 범위인지 확인하기](https://copyandrun.com/blog/dirty-pipe-kernel-version-range-check/) |
| [`dmarc-aggregate-report-xml-parse`](dmarc-aggregate-report-xml-parse/) | [DMARC 집계 보고서 읽기: rua XML을 파이썬으로 파싱해 SPF, DKIM 보기](https://copyandrun.com/blog/dmarc-aggregate-report-xml-parse/) |
| [`dockle-image-best-practice-check`](dockle-image-best-practice-check/) | [Dockle로 만들어진 컨테이너 이미지 점검하기: 비밀 노출, root 실행, 종료 코드 기준까지](https://copyandrun.com/blog/dockle-image-best-practice-check/) |
| [`elasticsearch-install-apt`](elasticsearch-install-apt/) | [Ubuntu에서 Elasticsearch 설치하고 기동하기](https://copyandrun.com/blog/elasticsearch-install-apt/) |
| [`elk-install-failures`](elk-install-failures/) | [ELK 설치가 실패하는 흔한 원인 세 가지와 해결](https://copyandrun.com/blog/elk-install-failures/) |
| [`elk-lab-server-docker`](elk-lab-server-docker/) | [Docker로 ELK 실습 서버 준비하기](https://copyandrun.com/blog/elk-lab-server-docker/) |
| [`elk-snapshot-backup`](elk-snapshot-backup/) | [ELK 스냅샷과 이미지로 백업하고 복구하기](https://copyandrun.com/blog/elk-snapshot-backup/) |
| [`entropy-upx-packed-detect`](entropy-upx-packed-detect/) | [엔트로피와 섹션 이름으로 패킹된 파일 가려내기: UPX 전후 비교](https://copyandrun.com/blog/entropy-upx-packed-detect/) |
| [`evidence-hash-chain-of-custody-record`](evidence-hash-chain-of-custody-record/) | [증거 파일 해시와 보관 기록(chain of custody) 만들기](https://copyandrun.com/blog/evidence-hash-chain-of-custody-record/) |
| [`fail2ban-sshd-ban-test`](fail2ban-sshd-ban-test/) | [fail2ban SSH 무차별 대입 차단: 3번 실패 차단과 40초 뒤 해제 확인](https://copyandrun.com/blog/fail2ban-sshd-ban-test/) |
| [`falco-container-runtime-rules`](falco-container-runtime-rules/) | [Falco 컨테이너 런타임 규칙 시험: 셸 실행, /etc 쓰기](https://copyandrun.com/blog/falco-container-runtime-rules/) |
| [`file-metadata-exif-office-author-strip`](file-metadata-exif-office-author-strip/) | [공유 전에 파일 속 숨은 정보 지우기: 사진 EXIF의 GPS와 Office 문서의 작성자 이름](https://copyandrun.com/blog/file-metadata-exif-office-author-strip/) |
| [`flask-attack-and-fix-own-app`](flask-attack-and-fix-own-app/) | [작은 Flask 서비스를 직접 공격하고 한 줄씩 고치기](https://copyandrun.com/blog/flask-attack-and-fix-own-app/) |
| [`flask-file-upload-hardening`](flask-file-upload-hardening/) | [Flask 파일 업로드 검증과 경로 조작 방어하기](https://copyandrun.com/blog/flask-file-upload-hardening/) |
| [`forensic-disk-image-timeline-sleuthkit`](forensic-disk-image-timeline-sleuthkit/) | [Sleuth Kit 디스크 이미지 파일 활동 시간표: fls, mactime](https://copyandrun.com/blog/forensic-disk-image-timeline-sleuthkit/) |
| [`forensic-memory-volatility3-process-list`](forensic-memory-volatility3-process-list/) | [Volatility 3 메모리 덤프 프로세스 목록 읽기: pslist, pstree](https://copyandrun.com/blog/forensic-memory-volatility3-process-list/) |
| [`gemini-api-python-first-call`](gemini-api-python-first-call/) | [Gemini API 파이썬으로 처음 호출하기: 키 보관, 첫 응답, 토큰 수, 오류 읽기](https://copyandrun.com/blog/gemini-api-python-first-call/) |
| [`gemini-api-streaming-chat-session`](gemini-api-streaming-chat-session/) | [Gemini API 스트리밍과 대화 세션: 첫 글자 시간 재고 이전 대화 기억시키기](https://copyandrun.com/blog/gemini-api-streaming-chat-session/) |
| [`gemini-api-system-instruction-json-schema`](gemini-api-system-instruction-json-schema/) | [Gemini API 시스템 지시와 JSON 스키마 출력: 로컬 모델과 같은 질문으로 비교](https://copyandrun.com/blog/gemini-api-system-instruction-json-schema/) |
| [`github-actions-hardening-zizmor-act`](github-actions-hardening-zizmor-act/) | [GitHub Actions 워크플로 하드닝: 위험 패턴 찾고 고치기](https://copyandrun.com/blog/github-actions-hardening-zizmor-act/) |
| [`grype-sbom-vulnerability-scan`](grype-sbom-vulnerability-scan/) | [Grype로 SBOM 취약점 점검하기: 심각도 집계와 종료 코드 게이트](https://copyandrun.com/blog/grype-sbom-vulnerability-scan/) |
| [`hadolint-dockerfile-lint`](hadolint-dockerfile-lint/) | [Hadolint로 Dockerfile 점검하기: 열한 가지 지적을 읽고 고치고, CI 기준 정하기](https://copyandrun.com/blog/hadolint-dockerfile-lint/) |
| [`hermes-agent-command-approval`](hermes-agent-command-approval/) | [Hermes Agent의 명령 승인 절차 확인하기](https://copyandrun.com/blog/hermes-agent-command-approval/) |
| [`hermes-agent-install-in-docker`](hermes-agent-install-in-docker/) | [Hermes Agent를 호스트가 아닌 Docker 컨테이너에 설치하고 첫 실행하기](https://copyandrun.com/blog/hermes-agent-install-in-docker/) |
| [`hermes-agent-local-ollama`](hermes-agent-local-ollama/) | [로컬 Ollama 모델을 Hermes Agent에 연결하기](https://copyandrun.com/blog/hermes-agent-local-ollama/) |
| [`hermes-agent-mcp-filesystem`](hermes-agent-mcp-filesystem/) | [Hermes Agent에 MCP filesystem 서버를 붙이고 접근 범위 제한하기](https://copyandrun.com/blog/hermes-agent-mcp-filesystem/) |
| [`hermes-agent-skills-and-memory`](hermes-agent-skills-and-memory/) | [Hermes Agent의 스킬과 메모리, 저장되는 정보 확인하기](https://copyandrun.com/blog/hermes-agent-skills-and-memory/) |
| [`hibp-k-anonymity-password-breach-check`](hibp-k-anonymity-password-breach-check/) | [Pwned Passwords 확인: Have I Been Pwned k-익명성 API 조회](https://copyandrun.com/blog/hibp-k-anonymity-password-breach-check/) |
| [`home-office-network-nmap-open-services-check`](home-office-network-nmap-open-services-check/) | [우리 사무실 네트워크에 열린 서비스 점검: nmap으로 기기별 포트 표 만들고 줄이기](https://copyandrun.com/blog/home-office-network-nmap-open-services-check/) |
| [`idor-ownership-check-flask`](idor-ownership-check-flask/) | [Flask에서 소유자 검사로 IDOR 막기](https://copyandrun.com/blog/idor-ownership-check-flask/) |
| [`isms-p-technical-checks-script-sample`](isms-p-technical-checks-script-sample/) | [ISMS-P 기술 점검 항목 일부를 스크립트로 확인해 양호, 취약, 수동확인 표 만들기](https://copyandrun.com/blog/isms-p-technical-checks-script-sample/) |
| [`java-deserialization-objectinputfilter`](java-deserialization-objectinputfilter/) | [Java 역직렬화 위험과 ObjectInputFilter: 허용한 클래스만 읽게 제한하기](https://copyandrun.com/blog/java-deserialization-objectinputfilter/) |
| [`java-emudhra-ca-cve-2026-91403-check`](java-emudhra-ca-cve-2026-91403-check/) | [CVE-2026-91403 점검: Java cacerts의 eMudhra 루트 인증서 확인과 삭제](https://copyandrun.com/blog/java-emudhra-ca-cve-2026-91403-check/) |
| [`java-jdbc-preparedstatement-sqli`](java-jdbc-preparedstatement-sqli/) | [Java JDBC SQL 인젝션 막기: PreparedStatement 비교](https://copyandrun.com/blog/java-jdbc-preparedstatement-sqli/) |
| [`java-spotbugs-findsecbugs-gate`](java-spotbugs-findsecbugs-gate/) | [SpotBugs와 Find Security Bugs로 Java 보안 점검 게이트 만들기](https://copyandrun.com/blog/java-spotbugs-findsecbugs-gate/) |
| [`jwt-validation-pitfalls`](jwt-validation-pitfalls/) | [JWT 검증 실수: 서명 확인 끄기, alg none, 알고리즘 혼동, 만료와 aud](https://copyandrun.com/blog/jwt-validation-pitfalls/) |
| [`k8s-networkpolicy-default-deny-kind`](k8s-networkpolicy-default-deny-kind/) | [Kubernetes NetworkPolicy 기본 거부: kind로 허용과 차단 확인](https://copyandrun.com/blog/k8s-networkpolicy-default-deny-kind/) |
| [`keycloak-oidc-pkce-local-login`](keycloak-oidc-pkce-local-login/) | [Keycloak 로컬 구성과 OIDC PKCE 로그인: 코드 가로채기 방어 확인](https://copyandrun.com/blog/keycloak-oidc-pkce-local-login/) |
| [`kibana-dashboard-geoip`](kibana-dashboard-geoip/) | [Kibana 대시보드와 GeoIP 지도로 접속 현황 보기](https://copyandrun.com/blog/kibana-dashboard-geoip/) |
| [`kibana-install-connect`](kibana-install-connect/) | [Kibana 설치하고 Elasticsearch에 연결하기](https://copyandrun.com/blog/kibana-install-connect/) |
| [`korean-pii-regex-presidio-scan`](korean-pii-regex-presidio-scan/) | [한국어 개인정보 찾기: 정규식과 Presidio 비교, 스캔 결과와 마스킹](https://copyandrun.com/blog/korean-pii-regex-presidio-scan/) |
| [`kubescape-pod-hardening-kind`](kubescape-pod-hardening-kind/) | [kubescape로 파드 설정 점검하고 kind에서 확인하기: 약한 파드와 단단한 파드 비교](https://copyandrun.com/blog/kubescape-pod-hardening-kind/) |
| [`linux-auth-log-ssh-intrusion-triage`](linux-auth-log-ssh-intrusion-triage/) | [auth.log로 SSH 침입 흔적 읽기: 실패 반복, 성공 로그인, 직후 sudo를 시간순으로](https://copyandrun.com/blog/linux-auth-log-ssh-intrusion-triage/) |
| [`llama-cpp-gpu-vs-cpu-ngl`](llama-cpp-gpu-vs-cpu-ngl/) | [llama.cpp -ngl로 그래픽 가속 켜고 끄기: 1B와 7B 속도 차이와 중간 값 측정](https://copyandrun.com/blog/llama-cpp-gpu-vs-cpu-ngl/) |
| [`llama-cpp-vulkan-bench-gguf`](llama-cpp-vulkan-bench-gguf/) | [llama.cpp와 GGUF 파일로 내 PC 속도 재기: llama-bench로 1B와 7B 비교](https://copyandrun.com/blog/llama-cpp-vulkan-bench-gguf/) |
| [`llama-server-json-schema-grammar`](llama-server-json-schema-grammar/) | [작은 모델의 출력 형식을 고정하기: llama-server의 JSON 스키마와 GBNF 문법](https://copyandrun.com/blog/llama-server-json-schema-grammar/) |
| [`llama-server-openai-compatible-api`](llama-server-openai-compatible-api/) | [llama-server로 내 PC에 OpenAI 호환 API 열기](https://copyandrun.com/blog/llama-server-openai-compatible-api/) |
| [`llm-agent-audit-log-opensearch`](llm-agent-audit-log-opensearch/) | [에이전트가 한 일을 추적하는 감사 로그: 호출마다 실행 주체와 도구를 남기기](https://copyandrun.com/blog/llm-agent-audit-log-opensearch/) |
| [`llm-agent-excessive-agency`](llm-agent-excessive-agency/) | [LLM 에이전트의 Excessive Agency: 취약한 도구와 최소 권한 도구 비교](https://copyandrun.com/blog/llm-agent-excessive-agency/) |
| [`local-ai-home-pc-model-size-guide`](local-ai-home-pc-model-size-guide/) | [집 PC에서 로컬 AI 돌리기: 메모리로 모델 크기 고르고 속도 재 보기](https://copyandrun.com/blog/local-ai-home-pc-model-size-guide/) |
| [`local-ca-openssl-leaf-cert-verify`](local-ca-openssl-leaf-cert-verify/) | [내 CA로 서버 인증서 발급하고 openssl verify 검증](https://copyandrun.com/blog/local-ca-openssl-leaf-cert-verify/) |
| [`local-llm-input-guardrail`](local-llm-input-guardrail/) | [Ollama 로컬 LLM에 입력 가드레일 붙이기](https://copyandrun.com/blog/local-llm-input-guardrail/) |
| [`local-llm-korean-model-comparison`](local-llm-korean-model-comparison/) | [한국어로 물어 본 로컬 모델 4종 비교: 2.4B, 3B, 27B, 31B](https://copyandrun.com/blog/local-llm-korean-model-comparison/) |
| [`local-rag-pdf-qa-ollama`](local-rag-pdf-qa-ollama/) | [Ollama와 로컬 RAG로 PDF에 묻고 답하기](https://copyandrun.com/blog/local-rag-pdf-qa-ollama/) |
| [`log4shell-anatomy-lookup-demo`](log4shell-anatomy-lookup-demo/) | [Log4Shell 해부: log4j 2.14.1과 2.17.1의 조회 해석 비교](https://copyandrun.com/blog/log4shell-anatomy-lookup-demo/) |
| [`logstash-grok-nginx-ecs`](logstash-grok-nginx-ecs/) | [Logstash로 nginx 로그를 Grok으로 파싱하고 ECS로 정규화하기](https://copyandrun.com/blog/logstash-grok-nginx-ecs/) |
| [`loki-promtail-log-query-logql`](loki-promtail-log-query-logql/) | [Loki로 nginx 로그 모으고 LogQL로 조회하기: 라벨 설계와 개인정보 마스킹](https://copyandrun.com/blog/loki-promtail-log-query-logql/) |
| [`lynis-container-host-audit`](lynis-container-host-audit/) | [Lynis로 리눅스 하드닝 점수 올려 보기: 우분투 컨테이너 보완 전후와 점수 게이트](https://copyandrun.com/blog/lynis-container-host-audit/) |
| [`mcp-rug-pull-tool-description-pinning`](mcp-rug-pull-tool-description-pinning/) | [MCP 도구 설명이 승인 뒤에 바뀌는 rug pull 탐지하기](https://copyandrun.com/blog/mcp-rug-pull-tool-description-pinning/) |
| [`misp-docker-ioc-import-export-stix`](misp-docker-ioc-import-export-stix/) | [MISP IOC 모으고 STIX 2.1로 내보내기: PyMISP](https://copyandrun.com/blog/misp-docker-ioc-import-export-stix/) |
| [`mkdocs-material-team-docs-site`](mkdocs-material-team-docs-site/) | [MkDocs Material로 팀 문서 사이트 만들기: 빌드, 엄격 모드, 로컬 미리보기](https://copyandrun.com/blog/mkdocs-material-team-docs-site/) |
| [`mongodb-auth-enabled-vs-open`](mongodb-auth-enabled-vs-open/) | [MongoDB 인증 켜기와 최소 권한 사용자: 열린 서버, 루트 공유, 역할 분리 비교](https://copyandrun.com/blog/mongodb-auth-enabled-vs-open/) |
| [`mysql-user-grants-audit`](mysql-user-grants-audit/) | [MySQL 8.0 사용자와 권한 감사: 빈 비밀번호, 와일드카드](https://copyandrun.com/blog/mysql-user-grants-audit/) |
| [`n8n-docker-webhook-workflow`](n8n-docker-webhook-workflow/) | [n8n으로 웹훅 자동화 만들기: 도커 실행, 워크플로 가져오기, 호출 확인](https://copyandrun.com/blog/n8n-docker-webhook-workflow/) |
| [`nginx-modsecurity-crs-block-test`](nginx-modsecurity-crs-block-test/) | [nginx ModSecurity와 OWASP CRS 웹 공격 차단 시험](https://copyandrun.com/blog/nginx-modsecurity-crs-block-test/) |
| [`nmap-scan-own-containers`](nmap-scan-own-containers/) | [Nmap으로 내 컨테이너 포트 점검하기: 열린 포트, 버전 확인, 스크립트 한 줄](https://copyandrun.com/blog/nmap-scan-own-containers/) |
| [`npm-supply-chain-install-script-defense`](npm-supply-chain-install-script-defense/) | [npm 설치 때 실행되는 스크립트를 막고 락파일 바뀐 곳 찾기](https://copyandrun.com/blog/npm-supply-chain-install-script-defense/) |
| [`ollama-embeddings-korean-similarity`](ollama-embeddings-korean-similarity/) | [Ollama 임베딩으로 한국어 문장 유사도 재기: 잘 되는 곳과 약한 곳](https://copyandrun.com/blog/ollama-embeddings-korean-similarity/) |
| [`ollama-expose-lan-risk-check`](ollama-expose-lan-risk-check/) | [Ollama를 0.0.0.0으로 열면 생기는 일: 인증 없는 로컬 AI 서버 점검](https://copyandrun.com/blog/ollama-expose-lan-risk-check/) |
| [`ollama-keep-alive-unload`](ollama-keep-alive-unload/) | [Ollama keep_alive: 모델을 메모리에 얼마나 올려 둘지 정하기](https://copyandrun.com/blog/ollama-keep-alive-unload/) |
| [`ollama-modelfile-custom-assistant`](ollama-modelfile-custom-assistant/) | [Ollama Modelfile로 말투와 길이가 고정된 나만의 도우미 모델 만들기](https://copyandrun.com/blog/ollama-modelfile-custom-assistant/) |
| [`ollama-num-ctx-memory-speed`](ollama-num-ctx-memory-speed/) | [Ollama num_ctx를 키우면 메모리는 얼마나 늘까: 2K, 8K, 32K 측정](https://copyandrun.com/blog/ollama-num-ctx-memory-speed/) |
| [`ollama-parallel-requests-throughput`](ollama-parallel-requests-throughput/) | [Ollama에 동시에 질문 여러 개 보내면: 1, 2, 4, 8개 요청 처리량 재기](https://copyandrun.com/blog/ollama-parallel-requests-throughput/) |
| [`ollama-python-api-json-streaming`](ollama-python-api-json-streaming/) | [파이썬에서 로컬 Ollama API 호출하기: 응답 받기, JSON 형식 고정, 스트리밍](https://copyandrun.com/blog/ollama-python-api-json-streaming/) |
| [`ollama-tool-calling-python`](ollama-tool-calling-python/) | [Ollama tool calling 파이썬 구현: 도구 호출, 인자 검증, 주입 지시 막기](https://copyandrun.com/blog/ollama-tool-calling-python/) |
| [`open-webui-ollama-connect-fix`](open-webui-ollama-connect-fix/) | [Open WebUI Ollama 연결: host.docker.internal:11434 고치기](https://copyandrun.com/blog/open-webui-ollama-connect-fix/) |
| [`openapi-schemathesis-api-fuzz-test`](openapi-schemathesis-api-fuzz-test/) | [OpenAPI 명세로 API 자동 시험: Schemathesis로 500 오류 찾기](https://copyandrun.com/blog/openapi-schemathesis-api-fuzz-test/) |
| [`openldap-acl-anonymous-vs-bound`](openldap-acl-anonymous-vs-bound/) | [OpenLDAP ACL 점검하기: 익명과 로그인 사용자가 비밀번호 해시를 읽을 수 있는지 확인](https://copyandrun.com/blog/openldap-acl-anonymous-vs-bound/) |
| [`opensearch-ollama-ai-siem`](opensearch-ollama-ai-siem/) | [Docker로 OpenSearch와 Ollama 띄워 비용 없는 AI-SIEM 만들기](https://copyandrun.com/blog/opensearch-ollama-ai-siem/) |
| [`os-command-injection-flask-subprocess`](os-command-injection-flask-subprocess/) | [OS 명령어 인젝션: ping 기능으로 보는 shell=True의 위험과 수정](https://copyandrun.com/blog/os-command-injection-flask-subprocess/) |
| [`osv-scanner-lockfile-vulnerabilities`](osv-scanner-lockfile-vulnerabilities/) | [OSV-Scanner로 잠금 파일 점검하기: 34건을 읽고, 예외를 두고, 0건이 될 때까지 고치기](https://copyandrun.com/blog/osv-scanner-lockfile-vulnerabilities/) |
| [`owasp-agentic-top10-mapped-to-hands-on`](owasp-agentic-top10-mapped-to-hands-on/) | [OWASP 에이전트 앱 Top 10을 내가 해 본 실습 결과에 대응시키기](https://copyandrun.com/blog/owasp-agentic-top10-mapped-to-hands-on/) |
| [`pandoc-markdown-to-docx`](pandoc-markdown-to-docx/) | [Pandoc으로 마크다운을 Word와 HTML로 바꾸기: 한글 문서 변환 확인](https://copyandrun.com/blog/pandoc-markdown-to-docx/) |
| [`passkey-webauthn-flask-virtual-authenticator`](passkey-webauthn-flask-virtual-authenticator/) | [패스키(WebAuthn)를 Flask에 붙이기: 가상 인증기로 등록과 로그인 확인](https://copyandrun.com/blog/passkey-webauthn-flask-virtual-authenticator/) |
| [`pe-header-imports-pefile-read`](pe-header-imports-pefile-read/) | [pefile로 실행 파일 구조 읽기: 헤더, 섹션, 임포트 표에서 보이는 것](https://copyandrun.com/blog/pe-header-imports-pefile-read/) |
| [`phishing-email-header-analysis-python`](phishing-email-header-analysis-python/) | [피싱 메일 헤더 분석: Received, SPF·DKIM·DMARC를 파이썬으로 점검](https://copyandrun.com/blog/phishing-email-header-analysis-python/) |
| [`pii-masking-logs-and-llm-prompts`](pii-masking-logs-and-llm-prompts/) | [로그와 LLM 프롬프트의 개인정보 마스킹: 주민번호·전화번호 패턴과 점검표](https://copyandrun.com/blog/pii-masking-logs-and-llm-prompts/) |
| [`pip-audit-python-dependencies`](pip-audit-python-dependencies/) | [pip-audit로 파이썬 의존성 취약점 점검하기: 고칠 버전과 종료 코드](https://copyandrun.com/blog/pip-audit-python-dependencies/) |
| [`pip-require-hashes-lockfile-pip-audit`](pip-require-hashes-lockfile-pip-audit/) | [pip 의존성에 해시를 고정하고 취약점 점검하기](https://copyandrun.com/blog/pip-require-hashes-lockfile-pip-audit/) |
| [`postfix-opendkim-sign-verify-local`](postfix-opendkim-sign-verify-local/) | [Postfix와 OpenDKIM으로 DKIM 서명하고 검증하기](https://copyandrun.com/blog/postfix-opendkim-sign-verify-local/) |
| [`postgres-pgcrypto-column-encrypt-masking-view`](postgres-pgcrypto-column-encrypt-masking-view/) | [pgcrypto로 컬럼 암호화하고 마스킹 뷰로 역할별 출력 나누기: 키가 서버 로그에 남는 문제까지](https://copyandrun.com/blog/postgres-pgcrypto-column-encrypt-masking-view/) |
| [`postgres-roles-least-privilege`](postgres-roles-least-privilege/) | [PostgreSQL 역할 최소 권한 실습: PUBLIC 회수, 기본 권한](https://copyandrun.com/blog/postgres-roles-least-privilege/) |
| [`postgres-row-level-security`](postgres-row-level-security/) | [PostgreSQL 행 수준 보안(RLS) 실습: 기본 거부, FORCE](https://copyandrun.com/blog/postgres-row-level-security/) |
| [`postgres-scram-pg-hba-test`](postgres-scram-pg-hba-test/) | [PostgreSQL pg_hba.conf 점검: trust를 SCRAM과 접속 제한으로 바꾸기](https://copyandrun.com/blog/postgres-scram-pg-hba-test/) |
| [`powershell-obfuscation-decode-ai-explain`](powershell-obfuscation-decode-ai-explain/) | [난독화한 PowerShell 한 줄 풀어 읽기: 직접 푼 결과와 생성형 AI 설명 비교](https://copyandrun.com/blog/powershell-obfuscation-decode-ai-explain/) |
| [`printnightmare-spooler-point-and-print-check`](printnightmare-spooler-point-and-print-check/) | [PrintNightmare 점검: Print Spooler와 Point and Print 정책 확인](https://copyandrun.com/blog/printnightmare-spooler-point-and-print-check/) |
| [`prometheus-alert-rules-promtool-test`](prometheus-alert-rules-promtool-test/) | [Prometheus 알림 규칙 promtool 단위 시험](https://copyandrun.com/blog/prometheus-alert-rules-promtool-test/) |
| [`prompt-injection-embedding-detector`](prompt-injection-embedding-detector/) | [임베딩 유사도로 프롬프트 인젝션 문장을 걸러 보기](https://copyandrun.com/blog/prompt-injection-embedding-detector/) |
| [`pwnkit-pkexec-patched-version-check`](pwnkit-pkexec-patched-version-check/) | [PwnKit 점검: pkexec 버전이 0.105여도 패치됐는지 변경 이력으로 확인하기](https://copyandrun.com/blog/pwnkit-pkexec-patched-version-check/) |
| [`python-password-hash-and-secrets`](python-password-hash-and-secrets/) | [파이썬 비밀번호 해시와 하드코딩된 시크릿 정리하기](https://copyandrun.com/blog/python-password-hash-and-secrets/) |
| [`rag-poisoning-indirect-injection`](rag-poisoning-indirect-injection/) | [RAG 포이즈닝과 간접 프롬프트 인젝션을 로컬에서 재현하기](https://copyandrun.com/blog/rag-poisoning-indirect-injection/) |
| [`redis-acl-users-commands`](redis-acl-users-commands/) | [Redis ACL로 사용자별 명령과 키 제한하기](https://copyandrun.com/blog/redis-acl-users-commands/) |
| [`restic-encrypted-backup-restore`](restic-encrypted-backup-restore/) | [restic으로 암호화 백업 만들기: 증가분 저장, 복원 검증, 손상 감지까지](https://copyandrun.com/blog/restic-encrypted-backup-restore/) |
| [`sca-sbom-practice`](sca-sbom-practice/) | [취약한 의존성 스캔하고 CycloneDX SBOM 만들기](https://copyandrun.com/blog/sca-sbom-practice/) |
| [`security-headers-nginx-before-after`](security-headers-nginx-before-after/) | [nginx 보안 헤더 설정 전후 비교: add_header가 404와 일부 경로에서 빠지는 함정](https://copyandrun.com/blog/security-headers-nginx-before-after/) |
| [`semgrep-custom-rule-python`](semgrep-custom-rule-python/) | [Semgrep으로 우리 팀 규칙 만들기: 파이썬 사용자 규칙 여섯 개와 규칙 시험](https://copyandrun.com/blog/semgrep-custom-rule-python/) |
| [`shellshock-bash-function-env-test`](shellshock-bash-function-env-test/) | [Shellshock 점검: bash 환경 변수 함수 정의 뒤의 명령이 실행되는지 안전하게 확인하기](https://copyandrun.com/blog/shellshock-bash-function-env-test/) |
| [`siem-log-quality-checks`](siem-log-quality-checks/) | [SIEM에 들어온 로그가 믿을 만한지 점검하기: 유실, 중복, 시간 어긋남](https://copyandrun.com/blog/siem-log-quality-checks/) |
| [`sigma-rule-to-elastic`](sigma-rule-to-elastic/) | [Sigma 룰을 작성하고 Elasticsearch 쿼리로 변환해 탐지하기](https://copyandrun.com/blog/sigma-rule-to-elastic/) |
| [`sops-age-encrypted-config`](sops-age-encrypted-config/) | [sops와 age로 설정 파일의 비밀만 암호화하기: 저장소에 올려도 되는 비밀 관리](https://copyandrun.com/blog/sops-age-encrypted-config/) |
| [`spf-dkim-dmarc-record-check-local-dns`](spf-dkim-dmarc-record-check-local-dns/) | [SPF, DKIM, DMARC 기록 읽고 점검하기: 파이썬](https://copyandrun.com/blog/spf-dkim-dmarc-record-check-local-dns/) |
| [`spf-lookup-limit-10-count`](spf-lookup-limit-10-count/) | [SPF 조회 10회 한도 점검: include와 DNS 조회 횟수 세기](https://copyandrun.com/blog/spf-lookup-limit-10-count/) |
| [`sql-parameter-binding-flask`](sql-parameter-binding-flask/) | [Flask에서 SQL 쿼리를 파라미터 바인딩으로 고치기](https://copyandrun.com/blog/sql-parameter-binding-flask/) |
| [`ssh-audit-sshd-hardening`](ssh-audit-sshd-hardening/) | [ssh-audit으로 sshd 암호 설정 점검하기: 약한 설정과 하드닝 설정 비교](https://copyandrun.com/blog/ssh-audit-sshd-hardening/) |
| [`ssh-server-hardening-ubuntu-sshd-config`](ssh-server-hardening-ubuntu-sshd-config/) | [Ubuntu SSH 서버 설정 점검: sshd -T로 유효 설정을 확인하고 암호 로그인을 끄는 방법](https://copyandrun.com/blog/ssh-server-hardening-ubuntu-sshd-config/) |
| [`ssrf-url-fetch-allowlist-flask`](ssrf-url-fetch-allowlist-flask/) | [SSRF 막기: URL 미리보기 기능에서 내부 주소 접근 차단](https://copyandrun.com/blog/ssrf-url-fetch-allowlist-flask/) |
| [`strings-floss-obfuscated-strings`](strings-floss-obfuscated-strings/) | [strings와 FLOSS로 문자열 꺼내기: 평문, 인코딩, 실행 중에 조립하는 문자열](https://copyandrun.com/blog/strings-floss-obfuscated-strings/) |
| [`sudo-baron-samedit-patched-version-check`](sudo-baron-samedit-patched-version-check/) | [sudo CVE-2021-3156 점검: 버전 1.8.31이어도 패치됐는지 변경 이력으로 확인하기](https://copyandrun.com/blog/sudo-baron-samedit-patched-version-check/) |
| [`sudoers-audit-nopasswd-wildcard`](sudoers-audit-nopasswd-wildcard/) | [sudoers 점검: NOPASSWD, 와일드카드, 셸 탈출 규칙 찾아 고치기](https://copyandrun.com/blog/sudoers-audit-nopasswd-wildcard/) |
| [`suricata-pcap-replay-alerts`](suricata-pcap-replay-alerts/) | [Suricata로 pcap 파일 재생해 보기: 사용자 규칙과 alert 개수 게이트](https://copyandrun.com/blog/suricata-pcap-replay-alerts/) |
| [`syft-sbom-container-image`](syft-sbom-container-image/) | [Syft로 컨테이너 이미지의 SBOM 만들기: 패키지 목록을 파일로 남기는 법](https://copyandrun.com/blog/syft-sbom-container-image/) |
| [`sysmon-process-tree-office-powershell`](sysmon-process-tree-office-powershell/) | [Sysmon 프로세스 생성 로그로 부모 자식 트리 그리기: 문서 앱이 셸을 띄우는 모양 찾기](https://copyandrun.com/blog/sysmon-process-tree-office-powershell/) |
| [`testssl-local-tls-check`](testssl-local-tls-check/) | [testssl.sh로 내 서버의 TLS 설정 점검하기: 약한 서버와 고친 서버를 같은 기준으로 비교](https://copyandrun.com/blog/testssl-local-tls-check/) |
| [`trivy-image-scan-gate`](trivy-image-scan-gate/) | [Trivy로 컨테이너 이미지 취약점을 스캔하고 빌드 게이트 만들기](https://copyandrun.com/blog/trivy-image-scan-gate/) |
| [`unquoted-service-path-check-powershell`](unquoted-service-path-check-powershell/) | [Windows 서비스 경로 따옴표 누락 점검: PowerShell로 찾기](https://copyandrun.com/blog/unquoted-service-path-check-powershell/) |
| [`uptime-kuma-docker-monitor`](uptime-kuma-docker-monitor/) | [Uptime Kuma로 서비스 상태 감시하기: 도커 실행, 감시 대상 추가, 정상과 장애 확인](https://copyandrun.com/blog/uptime-kuma-docker-monitor/) |
| [`urlhaus-feed-ioc-match-nginx-logs`](urlhaus-feed-ioc-match-nginx-logs/) | [URLhaus IOC 피드와 nginx 로그 대조하기](https://copyandrun.com/blog/urlhaus-feed-ioc-match-nginx-logs/) |
| [`vault-dev-mode-kv-policy`](vault-dev-mode-kv-policy/) | [HashiCorp Vault 개발 서버: KV 버전, 읽기 전용 정책](https://copyandrun.com/blog/vault-dev-mode-kv-policy/) |
| [`vaultwarden-self-host-backup`](vaultwarden-self-host-backup/) | [Vaultwarden으로 비밀번호 관리 서버 띄우기: 도커 실행, 상태 확인, 데이터 백업](https://copyandrun.com/blog/vaultwarden-self-host-backup/) |
| [`windows-bitlocker-tpm-secure-boot-check`](windows-bitlocker-tpm-secure-boot-check/) | [Windows 11 BitLocker, TPM, Secure Boot 상태 점검](https://copyandrun.com/blog/windows-bitlocker-tpm-secure-boot-check/) |
| [`windows-defender-eicar-detection-recheck`](windows-defender-eicar-detection-recheck/) | [Windows Defender EICAR 시험 파일 탐지 확인](https://copyandrun.com/blog/windows-defender-eicar-detection-recheck/) |
| [`windows-event-4624-logon-type-read`](windows-event-4624-logon-type-read/) | [Windows 이벤트 4624 로그온 유형으로 로컬, 네트워크, 서비스 로그온을 구분해 읽기](https://copyandrun.com/blog/windows-event-4624-logon-type-read/) |
| [`windows-event-4625-failed-logon-analysis`](windows-event-4625-failed-logon-analysis/) | [Windows 이벤트 4625 로그온 실패를 분석하고 계정 잠금 정책으로 대응하기](https://copyandrun.com/blog/windows-event-4625-failed-logon-analysis/) |
| [`windows-event-4672-special-privileges-logon`](windows-event-4672-special-privileges-logon/) | [Windows 이벤트 4672 특별 권한 로그온으로 관리자급 로그온을 찾고 일반 사용자와 비교하기](https://copyandrun.com/blog/windows-event-4672-special-privileges-logon/) |
| [`windows-event-4688-process-creation-audit`](windows-event-4688-process-creation-audit/) | [Windows 프로세스 만들기 감사와 명령줄 기록을 켜서 이벤트 4688로 실행 흔적 남기기](https://copyandrun.com/blog/windows-event-4688-process-creation-audit/) |
| [`windows-event-4720-account-lifecycle-4740-lockout`](windows-event-4720-account-lifecycle-4740-lockout/) | [Windows 이벤트 4720, 4725, 4726, 4740 계정 기록 읽기](https://copyandrun.com/blog/windows-event-4720-account-lifecycle-4740-lockout/) |
| [`windows-event-4732-local-admin-group-change`](windows-event-4732-local-admin-group-change/) | [Windows Administrators 그룹 변경 이벤트 4732 조회](https://copyandrun.com/blog/windows-event-4732-local-admin-group-change/) |
| [`windows-firewall-inbound-rule-block-recheck`](windows-firewall-inbound-rule-block-recheck/) | [Windows 방화벽 인바운드 차단 규칙: wf.msc로 만들고 이벤트 5152로 확인하기](https://copyandrun.com/blog/windows-firewall-inbound-rule-block-recheck/) |
| [`windows-lsa-protection-credential-guard-check`](windows-lsa-protection-credential-guard-check/) | [Windows LSA 보호와 Credential Guard(VBS) 켜짐 확인하기](https://copyandrun.com/blog/windows-lsa-protection-credential-guard-check/) |
| [`windows-powershell-script-block-logging-4104`](windows-powershell-script-block-logging-4104/) | [PowerShell 스크립트 블록 로깅을 켜서 이벤트 4104로 실행한 스크립트 내용 남기기](https://copyandrun.com/blog/windows-powershell-script-block-logging-4104/) |
| [`windows-run-key-startup-folder-persistence`](windows-run-key-startup-folder-persistence/) | [Windows Run 키와 시작 프로그램 폴더에 몰래 등록된 자동 실행 항목을 점검 스크립트로 찾기](https://copyandrun.com/blog/windows-run-key-startup-folder-persistence/) |
| [`windows-scheduled-task-persistence-4698`](windows-scheduled-task-persistence-4698/) | [Windows 작업 스케줄러에 몰래 생긴 작업을 이벤트 4698로 남기고 점검 스크립트로 찾기](https://copyandrun.com/blog/windows-scheduled-task-persistence-4698/) |
| [`windows-security-baseline-harden-recheck`](windows-security-baseline-harden-recheck/) | [Windows 보안 설정을 PowerShell로 점검하고 고친 뒤 다시 확인하기](https://copyandrun.com/blog/windows-security-baseline-harden-recheck/) |
| [`windows-service-7045-wmi-subscription-persistence`](windows-service-7045-wmi-subscription-persistence/) | [Windows 새 서비스 등록 이벤트 7045와 WMI 이벤트 구독을 점검 스크립트로 찾고 지우기](https://copyandrun.com/blog/windows-service-7045-wmi-subscription-persistence/) |
| [`windows-smb-hardening-check`](windows-smb-hardening-check/) | [Windows SMB 점검: SMBv1 끄기, 서명 요구, 공유 감사](https://copyandrun.com/blog/windows-smb-hardening-check/) |
| [`windows-smb-share-access-audit-5140`](windows-smb-share-access-audit-5140/) | [Windows 공유 폴더 접근 감사를 켜서 이벤트 5140과 5145로 누가 열었는지 남기기](https://copyandrun.com/blog/windows-smb-share-access-audit-5140/) |
| [`windows-sysmon-install-process-create-event-1`](windows-sysmon-install-process-create-event-1/) | [Sysmon 설치와 이벤트 1: 프로세스 해시와 부모 프로세스 기록, 4688 비교](https://copyandrun.com/blog/windows-sysmon-install-process-create-event-1/) |
| [`windows-sysmon-network-file-create-events-3-11`](windows-sysmon-network-file-create-events-3-11/) | [Sysmon 이벤트 3과 11로 PowerShell 내려받기 추적](https://copyandrun.com/blog/windows-sysmon-network-file-create-events-3-11/) |
| [`windows-update-server-air-gap-client-check`](windows-update-server-air-gap-client-check/) | [폐쇄망 Windows 업데이트 서버(WSUS) 구성과 클라이언트 점검](https://copyandrun.com/blog/windows-update-server-air-gap-client-check/) |
| [`wireguard-two-containers-handshake`](wireguard-two-containers-handshake/) | [WireGuard 터널 컨테이너 두 개로 만들기: 핸드셰이크](https://copyandrun.com/blog/wireguard-two-containers-handshake/) |
| [`xss-output-escaping-and-csp-flask`](xss-output-escaping-and-csp-flask/) | [XSS 막기: 출력 이스케이프와 CSP를 Flask에 적용하고 브라우저에서 확인](https://copyandrun.com/blog/xss-output-escaping-and-csp-flask/) |
| [`xz-backdoor-liblzma-version-check`](xz-backdoor-liblzma-version-check/) | [XZ 백도어 점검: xz 버전 5.6.0, 5.6.1 여부와 sshd의 liblzma 연결 확인하기](https://copyandrun.com/blog/xz-backdoor-liblzma-version-check/) |
| [`yara-rules-text-scan-python`](yara-rules-text-scan-python/) | [YARA 룰 작성과 파이썬 스캔: 문자열 조건으로 파일 분류하기](https://copyandrun.com/blog/yara-rules-text-scan-python/) |
| [`zap-baseline-scan-own-app`](zap-baseline-scan-own-app/) | [OWASP ZAP baseline 스캔으로 내 앱을 점검하고 보고서 읽기](https://copyandrun.com/blog/zap-baseline-scan-own-app/) |
| [`zeek-pcap-conn-http-logs`](zeek-pcap-conn-http-logs/) | [Zeek으로 pcap 읽어 conn.log와 http.log 만들기: 스캔 흔적과 404 개수 게이트](https://copyandrun.com/blog/zeek-pcap-conn-http-logs/) |

## 글 없이 올린 도구

| 폴더 | 내용 |
| --- | --- |
| [`java-runtime-inventory`](java-runtime-inventory/) | Java 런타임 현황 조사 도구 (sh, PowerShell) |

라이선스는 MIT 입니다.
