# Flask 파일 업로드 검증과 경로 조작 방어하기

원본 파일명을 그대로 저장하는 허술한 업로드가 폴더 밖에 파일을 남기는 것을 연습용 앱에서 확인합니다. 확장자 허용 목록, 크기 제한, 저장 이름 재생성, 경로 확인을 넣은 수정본에서 막히는 것까지 직접 확인합니다.

## 링크

- 글: [https://copyandrun.com/blog/flask-file-upload-hardening/](https://copyandrun.com/blog/flask-file-upload-hardening/)
- 한 번에 받기: [flask-file-upload-hardening.zip](https://copyandrun.com/code-zip/flask-file-upload-hardening.zip)
- GitHub 폴더: [copyandrun-labs/flask-file-upload-hardening](https://github.com/fankh/copyandrun-labs/tree/main/flask-file-upload-hardening)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `app.py` | <a href="https://fankh.github.io/copyandrun-labs/flask-file-upload-hardening/app.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/flask-file-upload-hardening/app.py) |
| `index.html` | <a href="https://fankh.github.io/copyandrun-labs/flask-file-upload-hardening/index.html" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/flask-file-upload-hardening/index.html) |
| `requirements.txt` | <a href="https://fankh.github.io/copyandrun-labs/flask-file-upload-hardening/requirements.txt" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/flask-file-upload-hardening/requirements.txt) |
| `vuln_app.py` | <a href="https://fankh.github.io/copyandrun-labs/flask-file-upload-hardening/vuln_app.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/flask-file-upload-hardening/vuln_app.py) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
