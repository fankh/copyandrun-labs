# 피싱 메일 헤더 분석: Received, SPF·DKIM·DMARC를 파이썬으로 점검

파이썬 표준 라이브러리 email 모듈로 .eml 파일을 읽어 Received 체인, Return-Path와 From 불일치, Reply-To 차이, Authentication-Results의 spf·dkim·dmarc 결과, 표시 이름 위장, 링크 표시 텍스트와 실제 주소 불일치를 점수 없이 항목별로 나열합니다. 직접 만든 시험 메일 3개(정상, 발신자 불일치형, 링크 위장형)로 결과를 대조하고 자동 점검의 한계도 정리합니다.

글: https://copyandrun.com/blog/phishing-email-header-analysis-python/

## 파일

- `analyze_eml.py`
- `make_samples.py`

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
