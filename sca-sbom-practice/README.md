# 취약한 의존성 스캔하고 CycloneDX SBOM 만들기

취약한 버전이 고정된 requirements.txt 하나로 pip-audit 스캔, CycloneDX SBOM 생성, Trivy 교차 확인, 버전 상향 후 재검증까지 해 봅니다. 마지막에는 같은 흐름을 PR마다 돌리는 GitHub Actions 워크플로를 붙입니다.

글: https://copyandrun.com/blog/sca-sbom-practice/

## 파일

- `report_view.py`
- `requirements.fixed.txt`
- `requirements.txt`
- `sca-sbom.yml`
- `show_sbom.py`

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
