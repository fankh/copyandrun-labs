# 공유 전에 파일 속 숨은 정보 지우기: 사진 EXIF의 GPS와 Office 문서의 작성자 이름

직접 만든 가짜 사진(JPEG)과 가짜 작성자 docx를 컨테이너에서 만들어, 촬영 기기와 시각과 GPS 좌표와 썸네일, 문서의 작성자와 마지막 수정자와 회사 이름이 어디에 남는지 읽고, 지운 사본을 만들어 다시 읽어 비교합니다. exiftool로 지워지지 않는 것과 스크립트로도 남는 것(썸네일, 본문 속 이름, 변경 추적, 파일 이름)도 직접 확인합니다.

## 링크

- 글: [https://copyandrun.com/blog/file-metadata-exif-office-author-strip/](https://copyandrun.com/blog/file-metadata-exif-office-author-strip/)
- 한 번에 받기: [file-metadata-exif-office-author-strip.zip](https://copyandrun.com/code-zip/file-metadata-exif-office-author-strip.zip)
- GitHub 폴더: [copyandrun-labs/file-metadata-exif-office-author-strip](https://github.com/fankh/copyandrun-labs/tree/main/file-metadata-exif-office-author-strip)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `clean_meta.py` | <a href="https://fankh.github.io/copyandrun-labs/file-metadata-exif-office-author-strip/clean_meta.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/file-metadata-exif-office-author-strip/clean_meta.py) |
| `compare_thumb.py` | <a href="https://fankh.github.io/copyandrun-labs/file-metadata-exif-office-author-strip/compare_thumb.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/file-metadata-exif-office-author-strip/compare_thumb.py) |
| `Dockerfile` | <a href="https://fankh.github.io/copyandrun-labs/file-metadata-exif-office-author-strip/Dockerfile" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/file-metadata-exif-office-author-strip/Dockerfile) |
| `inspect_meta.py` | <a href="https://fankh.github.io/copyandrun-labs/file-metadata-exif-office-author-strip/inspect_meta.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/file-metadata-exif-office-author-strip/inspect_meta.py) |
| `make_samples.py` | <a href="https://fankh.github.io/copyandrun-labs/file-metadata-exif-office-author-strip/make_samples.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/file-metadata-exif-office-author-strip/make_samples.py) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
