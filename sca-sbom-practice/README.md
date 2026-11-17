# 취약한 의존성 스캔하고 CycloneDX SBOM 만들기

취약한 버전이 고정된 requirements.txt 하나로 pip-audit 스캔, CycloneDX SBOM 생성, Trivy 교차 확인, 버전 상향 후 재검증까지 해 봅니다. 마지막에는 같은 절차를 PR마다 돌리는 GitHub Actions 워크플로를 붙입니다.

## 링크

- 글: [https://copyandrun.com/blog/sca-sbom-practice/](https://copyandrun.com/blog/sca-sbom-practice/)
- 한 번에 받기: [sca-sbom-practice.zip](https://copyandrun.com/code-zip/sca-sbom-practice.zip)
- GitHub 폴더: [copyandrun-labs/sca-sbom-practice](https://github.com/fankh/copyandrun-labs/tree/main/sca-sbom-practice)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `report_view.py` | <a href="https://fankh.github.io/copyandrun-labs/sca-sbom-practice/report_view.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/sca-sbom-practice/report_view.py) |
| `requirements.fixed.txt` | <a href="https://fankh.github.io/copyandrun-labs/sca-sbom-practice/requirements.fixed.txt" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/sca-sbom-practice/requirements.fixed.txt) |
| `requirements.txt` | <a href="https://fankh.github.io/copyandrun-labs/sca-sbom-practice/requirements.txt" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/sca-sbom-practice/requirements.txt) |
| `sca-sbom.yml` | <a href="https://fankh.github.io/copyandrun-labs/sca-sbom-practice/sca-sbom.yml" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/sca-sbom-practice/sca-sbom.yml) |
| `show_sbom.py` | <a href="https://fankh.github.io/copyandrun-labs/sca-sbom-practice/show_sbom.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/sca-sbom-practice/show_sbom.py) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
