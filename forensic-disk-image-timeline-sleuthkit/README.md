# Sleuth Kit 디스크 이미지 파일 활동 시간표: fls, mactime

mke2fs -d 로 직접 만든 작은 ext4 이미지에서 fls 본문 파일과 mactime 시간표를 만들고, 파일의 생성, 수정, 삭제 흔적이 시간표에 어떻게 나타나는지 확인합니다. istat 으로 삭제 시각을 보고 icat 으로 삭제한 시험 파일을 꺼내 보되(debugfs 로 지운 경우라 실제 삭제에서는 복구되지 않을 수 있습니다), 원본 해시를 먼저 기록하고 사본에서 작업하는 습관도 함께 다룹니다.

## 링크

- 글: [https://copyandrun.com/blog/forensic-disk-image-timeline-sleuthkit/](https://copyandrun.com/blog/forensic-disk-image-timeline-sleuthkit/)
- 한 번에 받기: [forensic-disk-image-timeline-sleuthkit.zip](https://copyandrun.com/code-zip/forensic-disk-image-timeline-sleuthkit.zip)
- GitHub 폴더: [copyandrun-labs/forensic-disk-image-timeline-sleuthkit](https://github.com/fankh/copyandrun-labs/tree/main/forensic-disk-image-timeline-sleuthkit)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `analyze.sh` | <a href="https://fankh.github.io/copyandrun-labs/forensic-disk-image-timeline-sleuthkit/analyze.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/forensic-disk-image-timeline-sleuthkit/analyze.sh) |
| `Dockerfile` | <a href="https://fankh.github.io/copyandrun-labs/forensic-disk-image-timeline-sleuthkit/Dockerfile" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/forensic-disk-image-timeline-sleuthkit/Dockerfile) |
| `make_image.sh` | <a href="https://fankh.github.io/copyandrun-labs/forensic-disk-image-timeline-sleuthkit/make_image.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/forensic-disk-image-timeline-sleuthkit/make_image.sh) |
| `timeline_summary.py` | <a href="https://fankh.github.io/copyandrun-labs/forensic-disk-image-timeline-sleuthkit/timeline_summary.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/forensic-disk-image-timeline-sleuthkit/timeline_summary.py) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
