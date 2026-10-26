# Checkov로 Terraform 설정 오류를 찾고 고치기

연습용 main.tf를 apply 없이 Checkov로 점검해 실패 항목 표를 읽고, 설정을 고쳐 통과시킵니다. 사유를 남기는 skip 주석, soft-fail과 종료 코드로 만드는 CI 게이트, json과 sarif 출력, Trivy config와의 결과 비교까지 다룹니다.

글: https://copyandrun.com/blog/checkov-terraform-misconfig/

## 파일

- `bad-main.tf`
- `checkov_view.py`
- `fixed-main.tf`
- `weak-main.tf`

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
