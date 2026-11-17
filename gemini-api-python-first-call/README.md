# Gemini API 파이썬으로 처음 호출하기: 키 보관, 첫 응답, 토큰 수, 오류 읽기

google-genai 라이브러리를 설치하고 API 키를 환경 변수로 보관한 뒤 gemini-2.5-flash-lite를 한 번 호출합니다. 응답의 토큰 사용량, count_tokens, 모델 이름을 틀렸을 때의 404와 키가 틀렸을 때의 400 오류까지 직접 확인합니다.

글: https://copyandrun.com/blog/gemini-api-python-first-call/

## 파일

- `first_call.py`
- `gemini_more.py`

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
