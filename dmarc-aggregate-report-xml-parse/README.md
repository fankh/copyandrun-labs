# DMARC 집계 보고서 읽기: rua XML을 파이썬으로 파싱해 SPF, DKIM 보기

DMARC 정책을 p=none으로 시작하면 수신 서버가 rua 주소로 XML 집계 보고서를 보냅니다. 이 XML을 Python 표준 라이브러리만으로 읽어 발신 IP별 SPF, DKIM, DMARC 통과 여부와 실패 비율을 요약하는 스크립트를 만들고 시험 보고서로 실행합니다.

## 링크

- 글: [https://copyandrun.com/blog/dmarc-aggregate-report-xml-parse/](https://copyandrun.com/blog/dmarc-aggregate-report-xml-parse/)
- 한 번에 받기: [dmarc-aggregate-report-xml-parse.zip](https://copyandrun.com/code-zip/dmarc-aggregate-report-xml-parse.zip)
- GitHub 폴더: [copyandrun-labs/dmarc-aggregate-report-xml-parse](https://github.com/fankh/copyandrun-labs/tree/main/dmarc-aggregate-report-xml-parse)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `dmarc_summary.py` | <a href="https://fankh.github.io/copyandrun-labs/dmarc-aggregate-report-xml-parse/dmarc_summary.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/dmarc-aggregate-report-xml-parse/dmarc_summary.py) |
| `sample-dmarc-report.xml` | <a href="https://fankh.github.io/copyandrun-labs/dmarc-aggregate-report-xml-parse/sample-dmarc-report.xml" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/dmarc-aggregate-report-xml-parse/sample-dmarc-report.xml) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
