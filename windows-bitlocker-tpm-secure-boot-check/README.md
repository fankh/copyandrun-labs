# Windows 11 BitLocker, TPM, Secure Boot 상태 점검

Windows 11에서 디스크 암호화(BitLocker), TPM, Secure Boot가 켜져 있는지 PowerShell 스크립트 한 번으로 읽고, 이 PC에서 BitLocker와 Secure Boot가 꺼져 있다는 결과가 무엇을 뜻하는지 판단하는 방법을 정리합니다.

## 링크

- 글: [https://copyandrun.com/blog/windows-bitlocker-tpm-secure-boot-check/](https://copyandrun.com/blog/windows-bitlocker-tpm-secure-boot-check/)
- 한 번에 받기: [windows-bitlocker-tpm-secure-boot-check.zip](https://copyandrun.com/code-zip/windows-bitlocker-tpm-secure-boot-check.zip)
- GitHub 폴더: [copyandrun-labs/windows-bitlocker-tpm-secure-boot-check](https://github.com/fankh/copyandrun-labs/tree/main/windows-bitlocker-tpm-secure-boot-check)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `Get-BootProtection.ps1` | <a href="https://fankh.github.io/copyandrun-labs/windows-bitlocker-tpm-secure-boot-check/Get-BootProtection.ps1" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/windows-bitlocker-tpm-secure-boot-check/Get-BootProtection.ps1) |
| `Test-BitLockerProtectors.ps1` | <a href="https://fankh.github.io/copyandrun-labs/windows-bitlocker-tpm-secure-boot-check/Test-BitLockerProtectors.ps1" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/windows-bitlocker-tpm-secure-boot-check/Test-BitLockerProtectors.ps1) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
