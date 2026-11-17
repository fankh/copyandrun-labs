# Dirty Pipe 점검: 커널 버전이 CVE-2022-0847 영향 범위인지 확인하기

Dirty Pipe(CVE-2022-0847)는 커널 5.8부터 5.10.102, 5.15.25, 5.16.11 이전 구간이 영향 범위입니다. 커널 버전을 NVD 범위와 비교하는 스크립트를 만들고, 경계값에서 판정이 바뀌는 것을 확인합니다. 컨테이너는 호스트 커널을 쓰는 점도 함께 짚습니다.

## 링크

- 글: [https://copyandrun.com/blog/dirty-pipe-kernel-version-range-check/](https://copyandrun.com/blog/dirty-pipe-kernel-version-range-check/)
- 한 번에 받기: [dirty-pipe-kernel-version-range-check.zip](https://copyandrun.com/code-zip/dirty-pipe-kernel-version-range-check.zip)
- GitHub 폴더: [copyandrun-labs/dirty-pipe-kernel-version-range-check](https://github.com/fankh/copyandrun-labs/tree/main/dirty-pipe-kernel-version-range-check)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `dirtypipe-check.sh` | <a href="https://fankh.github.io/copyandrun-labs/dirty-pipe-kernel-version-range-check/dirtypipe-check.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/dirty-pipe-kernel-version-range-check/dirtypipe-check.sh) |
| `dirtypipe-lab.sh` | <a href="https://fankh.github.io/copyandrun-labs/dirty-pipe-kernel-version-range-check/dirtypipe-lab.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/dirty-pipe-kernel-version-range-check/dirtypipe-lab.sh) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
