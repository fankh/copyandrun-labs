# Copy & Run 실습 코드

[https://copyandrun.com](https://copyandrun.com) 의 글에서 쓰는 실습 코드 모음입니다. 폴더 이름이 글 주소의 마지막 부분과 같습니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다.

| 폴더 | 글 |
| --- | --- |
| [`agent-config-hidden-instructions-scan`](agent-config-hidden-instructions-scan/) | [저장소의 에이전트 설정 파일에 숨은 지시 찾아내기](https://copyandrun.com/blog/agent-config-hidden-instructions-scan/) |
| [`checkov-terraform-misconfig`](checkov-terraform-misconfig/) | [Checkov로 Terraform 설정 오류를 찾고 고치기](https://copyandrun.com/blog/checkov-terraform-misconfig/) |
| [`ci-semgrep-bandit-gate`](ci-semgrep-bandit-gate/) | [CI에 Semgrep과 Bandit 보안 게이트 붙이기](https://copyandrun.com/blog/ci-semgrep-bandit-gate/) |
| [`cosign-image-signing-local-registry`](cosign-image-signing-local-registry/) | [컨테이너 이미지에 서명하고 서명 없는 이미지 거부하기(cosign)](https://copyandrun.com/blog/cosign-image-signing-local-registry/) |
| [`elasticsearch-install-apt`](elasticsearch-install-apt/) | [Ubuntu에서 Elasticsearch 설치하고 기동하기](https://copyandrun.com/blog/elasticsearch-install-apt/) |
| [`elk-install-failures`](elk-install-failures/) | [ELK 설치가 실패하는 흔한 원인 세 가지와 해결](https://copyandrun.com/blog/elk-install-failures/) |
| [`elk-lab-server-docker`](elk-lab-server-docker/) | [Docker로 ELK 실습 서버 준비하기](https://copyandrun.com/blog/elk-lab-server-docker/) |
| [`elk-snapshot-backup`](elk-snapshot-backup/) | [ELK 스냅샷과 이미지로 백업하고 복구하기](https://copyandrun.com/blog/elk-snapshot-backup/) |
| [`flask-attack-and-fix-own-app`](flask-attack-and-fix-own-app/) | [작은 Flask 서비스를 직접 공격하고 한 줄씩 고치기](https://copyandrun.com/blog/flask-attack-and-fix-own-app/) |
| [`flask-file-upload-hardening`](flask-file-upload-hardening/) | [Flask 파일 업로드 검증과 경로 조작 방어하기](https://copyandrun.com/blog/flask-file-upload-hardening/) |
| [`github-actions-hardening-zizmor-act`](github-actions-hardening-zizmor-act/) | [GitHub Actions 워크플로 하드닝: 위험 패턴 찾고 고치기](https://copyandrun.com/blog/github-actions-hardening-zizmor-act/) |
| [`hermes-agent-command-approval`](hermes-agent-command-approval/) | [Hermes Agent의 명령 승인 흐름 확인하기](https://copyandrun.com/blog/hermes-agent-command-approval/) |
| [`hermes-agent-install-in-docker`](hermes-agent-install-in-docker/) | [Hermes Agent를 호스트가 아닌 Docker 컨테이너에 설치하고 첫 실행하기](https://copyandrun.com/blog/hermes-agent-install-in-docker/) |
| [`hermes-agent-local-ollama`](hermes-agent-local-ollama/) | [로컬 Ollama 모델을 Hermes Agent에 연결하기](https://copyandrun.com/blog/hermes-agent-local-ollama/) |
| [`hermes-agent-mcp-filesystem`](hermes-agent-mcp-filesystem/) | [Hermes Agent에 MCP filesystem 서버를 붙이고 접근 범위 제한하기](https://copyandrun.com/blog/hermes-agent-mcp-filesystem/) |
| [`hermes-agent-skills-and-memory`](hermes-agent-skills-and-memory/) | [Hermes Agent의 스킬과 메모리, 저장되는 정보 확인하기](https://copyandrun.com/blog/hermes-agent-skills-and-memory/) |
| [`idor-ownership-check-flask`](idor-ownership-check-flask/) | [Flask에서 소유자 검사로 IDOR 막기](https://copyandrun.com/blog/idor-ownership-check-flask/) |
| [`k8s-networkpolicy-default-deny-kind`](k8s-networkpolicy-default-deny-kind/) | [Kubernetes NetworkPolicy 기본 거부: kind로 허용과 차단 확인](https://copyandrun.com/blog/k8s-networkpolicy-default-deny-kind/) |
| [`keycloak-oidc-pkce-local-login`](keycloak-oidc-pkce-local-login/) | [Keycloak 로컬 구성과 OIDC PKCE 로그인: 코드 가로채기 방어 확인](https://copyandrun.com/blog/keycloak-oidc-pkce-local-login/) |
| [`kibana-dashboard-geoip`](kibana-dashboard-geoip/) | [Kibana 대시보드와 GeoIP 지도로 접속 현황 보기](https://copyandrun.com/blog/kibana-dashboard-geoip/) |
| [`kibana-install-connect`](kibana-install-connect/) | [Kibana 설치하고 Elasticsearch에 연결하기](https://copyandrun.com/blog/kibana-install-connect/) |
| [`llm-agent-audit-log-opensearch`](llm-agent-audit-log-opensearch/) | [에이전트가 한 일을 추적하는 감사 로그: 호출마다 실행 주체와 도구를 남기기](https://copyandrun.com/blog/llm-agent-audit-log-opensearch/) |
| [`llm-agent-excessive-agency`](llm-agent-excessive-agency/) | [LLM 에이전트의 Excessive Agency: 취약한 도구와 최소 권한 도구 비교](https://copyandrun.com/blog/llm-agent-excessive-agency/) |
| [`local-llm-input-guardrail`](local-llm-input-guardrail/) | [Ollama 로컬 LLM에 입력 가드레일 붙이기](https://copyandrun.com/blog/local-llm-input-guardrail/) |
| [`local-rag-pdf-qa-ollama`](local-rag-pdf-qa-ollama/) | [Ollama와 로컬 RAG로 PDF에 묻고 답하기](https://copyandrun.com/blog/local-rag-pdf-qa-ollama/) |
| [`logstash-grok-nginx-ecs`](logstash-grok-nginx-ecs/) | [Logstash로 nginx 로그를 Grok으로 파싱하고 ECS로 정규화하기](https://copyandrun.com/blog/logstash-grok-nginx-ecs/) |
| [`mcp-rug-pull-tool-description-pinning`](mcp-rug-pull-tool-description-pinning/) | [MCP 도구 설명이 승인 뒤에 바뀌는 rug pull 탐지하기](https://copyandrun.com/blog/mcp-rug-pull-tool-description-pinning/) |
| [`npm-supply-chain-install-script-defense`](npm-supply-chain-install-script-defense/) | [npm 설치 때 실행되는 스크립트를 막고 락파일 바뀐 곳 찾기](https://copyandrun.com/blog/npm-supply-chain-install-script-defense/) |
| [`open-webui-ollama-connect-fix`](open-webui-ollama-connect-fix/) | [Open WebUI를 Docker로 띄워 Ollama에 연결하고 모델이 안 보일 때 고치기](https://copyandrun.com/blog/open-webui-ollama-connect-fix/) |
| [`opensearch-ollama-ai-siem`](opensearch-ollama-ai-siem/) | [Docker로 OpenSearch와 Ollama 띄워 비용 없는 AI-SIEM 만들기](https://copyandrun.com/blog/opensearch-ollama-ai-siem/) |
| [`os-command-injection-flask-subprocess`](os-command-injection-flask-subprocess/) | [OS 명령어 인젝션: ping 기능으로 보는 shell=True의 위험과 수정](https://copyandrun.com/blog/os-command-injection-flask-subprocess/) |
| [`owasp-agentic-top10-mapped-to-hands-on`](owasp-agentic-top10-mapped-to-hands-on/) | [OWASP 에이전트 앱 Top 10을 내가 해 본 실습 결과에 대응시키기](https://copyandrun.com/blog/owasp-agentic-top10-mapped-to-hands-on/) |
| [`passkey-webauthn-flask-virtual-authenticator`](passkey-webauthn-flask-virtual-authenticator/) | [패스키(WebAuthn)를 Flask에 붙이기: 가상 인증기로 등록과 로그인 확인](https://copyandrun.com/blog/passkey-webauthn-flask-virtual-authenticator/) |
| [`pii-masking-logs-and-llm-prompts`](pii-masking-logs-and-llm-prompts/) | [로그와 LLM 프롬프트의 개인정보 마스킹: 주민번호·전화번호 패턴과 점검표](https://copyandrun.com/blog/pii-masking-logs-and-llm-prompts/) |
| [`pip-require-hashes-lockfile-pip-audit`](pip-require-hashes-lockfile-pip-audit/) | [pip 의존성에 해시를 고정하고 취약점 점검하기](https://copyandrun.com/blog/pip-require-hashes-lockfile-pip-audit/) |
| [`prompt-injection-embedding-detector`](prompt-injection-embedding-detector/) | [임베딩 유사도로 프롬프트 인젝션 문장을 걸러 보기](https://copyandrun.com/blog/prompt-injection-embedding-detector/) |
| [`python-password-hash-and-secrets`](python-password-hash-and-secrets/) | [파이썬 비밀번호 해시와 하드코딩된 시크릿 정리하기](https://copyandrun.com/blog/python-password-hash-and-secrets/) |
| [`rag-poisoning-indirect-injection`](rag-poisoning-indirect-injection/) | [RAG 포이즈닝과 간접 프롬프트 인젝션을 로컬에서 재현하기](https://copyandrun.com/blog/rag-poisoning-indirect-injection/) |
| [`sca-sbom-practice`](sca-sbom-practice/) | [취약한 의존성 스캔하고 CycloneDX SBOM 만들기](https://copyandrun.com/blog/sca-sbom-practice/) |
| [`siem-log-quality-checks`](siem-log-quality-checks/) | [SIEM에 들어온 로그가 믿을 만한지 점검하기: 유실, 중복, 시간 어긋남](https://copyandrun.com/blog/siem-log-quality-checks/) |
| [`sigma-rule-to-elastic`](sigma-rule-to-elastic/) | [Sigma 룰을 작성하고 Elasticsearch 쿼리로 변환해 탐지하기](https://copyandrun.com/blog/sigma-rule-to-elastic/) |
| [`sql-parameter-binding-flask`](sql-parameter-binding-flask/) | [Flask에서 SQL 쿼리를 파라미터 바인딩으로 고치기](https://copyandrun.com/blog/sql-parameter-binding-flask/) |
| [`ssrf-url-fetch-allowlist-flask`](ssrf-url-fetch-allowlist-flask/) | [SSRF 막기: URL 미리보기 기능에서 내부 주소 접근 차단](https://copyandrun.com/blog/ssrf-url-fetch-allowlist-flask/) |
| [`trivy-image-scan-gate`](trivy-image-scan-gate/) | [Trivy로 컨테이너 이미지 취약점을 스캔하고 빌드 게이트 만들기](https://copyandrun.com/blog/trivy-image-scan-gate/) |
| [`windows-event-4625-failed-logon-analysis-lab-vm`](windows-event-4625-failed-logon-analysis-lab-vm/) | [Windows 이벤트 4625 로그온 실패를 분석하고 계정 잠금 정책으로 대응하기](https://copyandrun.com/blog/windows-event-4625-failed-logon-analysis-lab-vm/) |
| [`windows-security-baseline-harden-recheck`](windows-security-baseline-harden-recheck/) | [Windows 보안 설정을 PowerShell로 점검하고 고친 뒤 다시 확인하기](https://copyandrun.com/blog/windows-security-baseline-harden-recheck/) |
| [`xss-output-escaping-and-csp-flask`](xss-output-escaping-and-csp-flask/) | [XSS 막기: 출력 이스케이프와 CSP를 Flask에 적용하고 브라우저에서 확인](https://copyandrun.com/blog/xss-output-escaping-and-csp-flask/) |
| [`zap-baseline-scan-own-app`](zap-baseline-scan-own-app/) | [OWASP ZAP baseline 스캔으로 내 앱을 점검하고 보고서 읽기](https://copyandrun.com/blog/zap-baseline-scan-own-app/) |

라이선스는 MIT 입니다.
