# Java 런타임 현황 조사 도구 (sh, PowerShell)

서버와 PC 에 있는 Java 런타임을 모두 찾아 공급업체, 전체 빌드 버전, 아키텍처, 실행 중인 프로세스를 CSV 로 남깁니다. 디스크의 java 실행 파일, 실행 중인 프로세스, 실행 중인 도커 컨테이너 안을 함께 봅니다. 찾은 java 를 -version 으로 한 번씩 실행해 버전을 읽고, 그 밖에는 읽기만 합니다.

## 파일

- `java-inventory.ps1`
- `java-inventory.sh`

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
