# n8n으로 웹훅 자동화 만들기: 도커 실행, 워크플로 가져오기, 호출 확인

오픈소스 자동화 도구 n8n을 도커로 localhost에만 열어 띄우고, 웹훅을 받아 JSON을 돌려주는 워크플로를 명령줄로 가져와 게시합니다. 게시 전후의 차이, 재시작이 필요했던 점, 한글과 빈 입력과 GET 요청 결과를 확인합니다.

## 링크

- 글: [https://copyandrun.com/blog/n8n-docker-webhook-workflow/](https://copyandrun.com/blog/n8n-docker-webhook-workflow/)
- 한 번에 받기: [n8n-docker-webhook-workflow.zip](https://copyandrun.com/code-zip/n8n-docker-webhook-workflow.zip)
- GitHub 폴더: [copyandrun-labs/n8n-docker-webhook-workflow](https://github.com/fankh/copyandrun-labs/tree/main/n8n-docker-webhook-workflow)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `run_n8n.sh` | <a href="https://fankh.github.io/copyandrun-labs/n8n-docker-webhook-workflow/run_n8n.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/n8n-docker-webhook-workflow/run_n8n.sh) |
| `wf.json` | <a href="https://fankh.github.io/copyandrun-labs/n8n-docker-webhook-workflow/wf.json" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/n8n-docker-webhook-workflow/wf.json) |
| `wf2.json` | <a href="https://fankh.github.io/copyandrun-labs/n8n-docker-webhook-workflow/wf2.json" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/n8n-docker-webhook-workflow/wf2.json) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
