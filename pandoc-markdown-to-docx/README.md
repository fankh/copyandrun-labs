# Pandoc으로 마크다운을 Word와 HTML로 바꾸기: 한글 문서 변환 확인

마크다운 보고서를 pandoc/core 이미지로 docx와 html로 변환하고, docx를 압축 해제해 제목, 표, 굵은 글씨가 들어갔는지 확인합니다. PDF 변환은 LaTeX가 없어 실패한 결과 그대로 기록합니다.

글: https://copyandrun.com/blog/pandoc-markdown-to-docx/

## 파일

- `check_docx.py`
- `convert.sh`
- `pandoc_more.sh`
- `report.md`

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
