# kubescape로 파드 설정 점검하고 kind에서 확인하기: 약한 파드와 단단한 파드 비교

privileged에 root로 도는 파드와 비루트, 읽기 전용 파일시스템, 권한 전부 제거를 건 파드를 kubescape로 점검해 실패한 통제를 비교하고, 같은 두 파드를 kind의 Pod Security restricted 네임스페이스에 배포해 거절과 승인, 파드 안의 권한 차이를 직접 확인합니다.

## 링크

- 글: [https://copyandrun.com/blog/kubescape-pod-hardening-kind/](https://copyandrun.com/blog/kubescape-pod-hardening-kind/)
- 한 번에 받기: [kubescape-pod-hardening-kind.zip](https://copyandrun.com/code-zip/kubescape-pod-hardening-kind.zip)
- GitHub 폴더: [copyandrun-labs/kubescape-pod-hardening-kind](https://github.com/fankh/copyandrun-labs/tree/main/kubescape-pod-hardening-kind)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `hardened.yaml` | <a href="https://fankh.github.io/copyandrun-labs/kubescape-pod-hardening-kind/hardened.yaml" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/kubescape-pod-hardening-kind/hardened.yaml) |
| `ks_summary.py` | <a href="https://fankh.github.io/copyandrun-labs/kubescape-pod-hardening-kind/ks_summary.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/kubescape-pod-hardening-kind/ks_summary.py) |
| `kubescape_demo.sh` | <a href="https://fankh.github.io/copyandrun-labs/kubescape-pod-hardening-kind/kubescape_demo.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/kubescape-pod-hardening-kind/kubescape_demo.sh) |
| `weak.yaml` | <a href="https://fankh.github.io/copyandrun-labs/kubescape-pod-hardening-kind/weak.yaml" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/kubescape-pod-hardening-kind/weak.yaml) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
