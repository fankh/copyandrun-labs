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
| `latest_build` | 같은 공급업체, 같은 Java 버전의 최신 빌드와 그 배포일 ([endoflife.date](https://endoflife.date) 자료) |
| `status` | feature.interim.update 를 비교하고, 같으면 그 뒤 패치 번호(예: 21.0.13.0.3)까지 비교한 결과. 최신 / 업데이트 필요 / 지원 종료 / 확인 필요 (PowerShell 판은 영문) |
| `emudhra_roots` | cacerts 에 남은 eMudhra 루트 인증서. CVE-2026-91403, CVE-2026-114820 경보에서 지우라고 한 네 개를 CN 으로 찾습니다 |
| `java4shell` | Java4Shell(CVE-2026-114938) 영향 여부. JDK 17/21/25/27 이 마지막 영향 빌드(17.0.21.0.3, 21.0.13.0.3, 25.0.5.0.3, 27.0.1.0.3) 이하이고, CPU 가 AVX-512 VBMI 를 지원하는 x86-64 이면 영향 있음. 실행 중인 JVM 이 `-XX:UseAVX=0/1/2` 또는 `-XX:-UseBASE64Intrinsics` 로 임시 완화했는지도 표시 |

- `확인 필요` 는 공급업체 자료가 없거나(Azul, OS 패키지 등) 자료가 120일 넘게 갱신되지 않은 경우입니다. 해당 공급업체 공지로 직접 확인합니다.
- `최신` 은 괄호 안 날짜의 자료 기준입니다. Oracle 은 매달 셋째 화요일에 보안 패치를 내므로, 그 날짜 뒤 공급업체 공지가 있으면 직접 확인합니다. 런타임이 패치 번호 없이 같은 업데이트(예: 21.0.13)이고 공급업체에 뒤 패치 빌드가 있으면 `확인 필요` 로 표시합니다.
- eMudhra 처럼 인증서로 판단하는 경보는 `emudhra_roots` 열로 확인합니다.
- 인터넷이 막힌 서버에서는 `-x`(sh) 또는 `-Offline`(PowerShell)을 붙이면 조회 없이 목록과 eMudhra 확인만 합니다.
- `java4shell` 의 CPU 판정은 JVM 이 본 CPU 기능(`-Xlog:os+cpu`)을 쓰고, Java 8 처럼 안 되면 `/proc/cpuinfo` 를 봅니다. 임시 완화 옵션은 실행 중인 프로세스의 명령줄만 보며 `JAVA_TOOL_OPTIONS` 나 옵션 파일은 보지 않습니다. OpenJDK 기반 배포판은 빌드 번호 표기가 달라 수정 빌드도 `영향 있음` 으로 보일 수 있으니 공급업체 공지로 최종 확인합니다.
- 라이브러리(jar) 취약점은 이 도구가 보지 않습니다. SCA 도구로 따로 점검합니다.
