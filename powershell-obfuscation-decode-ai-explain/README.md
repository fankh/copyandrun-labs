# 난독화한 PowerShell 한 줄 풀어 읽기: 직접 푼 결과와 생성형 AI 설명 비교

호스트 이름을 출력할 뿐인 무해한 PowerShell 한 줄을 세 가지 방식으로 난독화하고, 풀기 단계에서는 실행하지 않고 파이썬과 컨테이너 안 PowerShell로 풉니다. 푼 결과를 로컬 생성형 AI의 설명과 비교해 맞은 곳과 틀린 곳을 기록하고, 의심스러운 PowerShell을 만났을 때의 점검 순서를 정리합니다.

글: https://copyandrun.com/blog/powershell-obfuscation-decode-ai-explain/

## 파일

- `ask_ai.py`
- `decode.py`
- `decode_only.ps1`
- `make_samples.py`

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
