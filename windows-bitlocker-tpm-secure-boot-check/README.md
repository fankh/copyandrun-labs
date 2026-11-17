# Windows 11 BitLocker, TPM, Secure Boot 상태 점검

Windows 11에서 디스크 암호화(BitLocker), TPM, Secure Boot가 켜져 있는지 PowerShell 스크립트 한 번으로 읽고, 이 PC에서 BitLocker와 Secure Boot가 꺼져 있다는 결과가 무엇을 뜻하는지 판단하는 방법을 정리합니다.

글: https://copyandrun.com/blog/windows-bitlocker-tpm-secure-boot-check/

## 파일

- `Get-BootProtection.ps1`
- `Test-BitLockerProtectors.ps1`

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
