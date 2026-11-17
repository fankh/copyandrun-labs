# Gemini API 스트리밍과 대화 세션: 첫 글자 시간 재고 이전 대화 기억시키기

generate_content_stream으로 답을 조각으로 받아 첫 조각이 오기까지의 시간을 재고, chats.create로 이전 대화를 기억하는 세션을 만듭니다. 매 호출이 독립이라는 점과 세션이 그 대화를 어떻게 이어 주는지 실행 결과로 확인합니다.

글: https://copyandrun.com/blog/gemini-api-streaming-chat-session/

## 파일

- `stream_chat.py`
- `stream_more.py`

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
