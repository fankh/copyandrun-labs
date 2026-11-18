# Java 런타임 현황 조사 도구 (sh, PowerShell)

서버와 PC 에 있는 Java 런타임을 모두 찾아 공급업체, 전체 빌드 버전, 아키텍처, 실행 중인 프로세스를 CSV 로 남기고, 런타임마다 지금 알려진 보안 문제를 확인합니다. 디스크의 java 실행 파일, 실행 중인 프로세스, 실행 중인 도커 컨테이너 안을 함께 봅니다. 찾은 java 를 -version 으로, keytool 을 -list 로 한 번씩 실행하고, 그 밖에는 읽기만 합니다.

## 링크

- GitHub 폴더: [copyandrun-labs/java-runtime-inventory](https://github.com/fankh/copyandrun-labs/tree/main/java-runtime-inventory)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `java-inventory.ps1` | <a href="https://fankh.github.io/copyandrun-labs/java-runtime-inventory/java-inventory.ps1" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/java-runtime-inventory/java-inventory.ps1) |
| `java-inventory.sh` | <a href="https://fankh.github.io/copyandrun-labs/java-runtime-inventory/java-inventory.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/java-runtime-inventory/java-inventory.sh) |

## 사용 방법

리눅스에서는 root 로 실행합니다.

```bash
sudo sh java-inventory.sh
```

Windows 에서는 관리자 PowerShell 에서 실행합니다. `-Quick` 을 붙이면 Program Files 같은 흔한 폴더만 찾습니다.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File java-inventory.ps1
```

결과는 `java-inventory-<호스트 이름>.csv` 에 남습니다. 컨테이너 안을 보지 않으려면 `-n`(sh) 또는 `-NoContainers`(PowerShell)를 붙입니다.

찾을 폴더를 여러 개 줄 때는 쉼표로 구분합니다: `-Roots C:\,D:\`

## 보안 점검 열

| 열 | 내용 |
| --- | --- |
| `latest_build` | 같은 공급업체, 같은 Java 버전의 최신 빌드 ([endoflife.date](https://endoflife.date) 자료) |
| `status` | 분기 보안 업데이트 수준(feature.interim.update) 비교 결과. 최신 / 업데이트 필요 / 지원 종료 / 확인 필요 (PowerShell 판은 영문) |
| `emudhra_roots` | cacerts 에 남은 eMudhra 루트 인증서. CVE-2026-91403, CVE-2026-114820 경보에서 지우라고 한 네 개를 CN 으로 찾습니다 |

- `확인 필요` 는 공급업체 자료가 없거나(Azul, OS 패키지 등) 자료가 120일 넘게 갱신되지 않은 경우입니다. 해당 공급업체 공지로 직접 확인합니다.
- `status` 는 분기 업데이트만 비교합니다. 분기 사이의 긴급 경보(eMudhra 등)는 `emudhra_roots` 열로 확인합니다.
- 인터넷이 막힌 서버에서는 `-x`(sh) 또는 `-Offline`(PowerShell)을 붙이면 조회 없이 목록과 eMudhra 확인만 합니다.
- 라이브러리(jar) 취약점은 이 도구가 보지 않습니다. SCA 도구로 따로 점검합니다.
