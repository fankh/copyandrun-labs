# Gemini API 스트리밍과 대화 세션: 첫 글자 시간 재고 이전 대화 기억시키기

generate_content_stream으로 답을 조각으로 받아 첫 조각이 오기까지의 시간을 재고, chats.create로 이전 대화를 기억하는 세션을 만듭니다. 매 호출이 독립이라는 점과 세션이 그 대화를 어떻게 이어 주는지 실행 결과로 확인합니다.

## 링크

- 글: [https://copyandrun.com/blog/gemini-api-streaming-chat-session/](https://copyandrun.com/blog/gemini-api-streaming-chat-session/)
- 한 번에 받기: [gemini-api-streaming-chat-session.zip](https://copyandrun.com/code-zip/gemini-api-streaming-chat-session.zip)
- GitHub 폴더: [copyandrun-labs/gemini-api-streaming-chat-session](https://github.com/fankh/copyandrun-labs/tree/main/gemini-api-streaming-chat-session)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `stream_chat.py` | <a href="https://fankh.github.io/copyandrun-labs/gemini-api-streaming-chat-session/stream_chat.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/gemini-api-streaming-chat-session/stream_chat.py) |
| `stream_more.py` | <a href="https://fankh.github.io/copyandrun-labs/gemini-api-streaming-chat-session/stream_more.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/gemini-api-streaming-chat-session/stream_more.py) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
