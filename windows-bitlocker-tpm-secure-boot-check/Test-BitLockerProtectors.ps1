# BitLocker 보호가 꺼진 시험용 PC에서 키 보호기를 추가하고 일시 중지와 다시 켜기를 해 보며 Get-BootProtection.ps1 의 결과를 본다.
# 주의: 시험용 PC에서만 실행한다. 복구 암호가 만들어지므로 실제 PC에서는 실행하지 않는다. 이 글의 값은 모두 시험용이다.
# 준비: 같은 폴더에 Get-BootProtection.ps1 이 있어야 한다. 관리자 PowerShell. 가상 머신이면 DVD(ISO)를 빼 둔다(아래 3번 참고).
# 출력 문구를 영어로 쓴 이유: Windows PowerShell 5.1 은 BOM 없는 UTF-8 파일의 한글 문자열을 깨뜨려 읽을 수 있다.
# 실행: powershell -NoProfile -ExecutionPolicy Bypass -File .\Test-BitLockerProtectors.ps1
Set-Location $PSScriptRoot
function Run { (powershell -NoProfile -ExecutionPolicy Bypass -File .\Get-BootProtection.ps1) | Where-Object { $_ -match 'C:|key protectors' } }

"## 1. Initial state"
Run

"## 2. Resume-BitLocker without any key protector"
try { Resume-BitLocker -MountPoint C: -ErrorAction Stop | Out-Null } catch { "  error: " + $_.Exception.Message.Split('(')[0].Trim() }

"## 3. Add a TPM protector and a recovery password protector, then resume"
# 부팅 가능한 DVD 가 연결되어 있으면 TPM 보호기 추가가 0x80310030 으로 실패한다. 그러면 DVD 를 빼고 다시 실행한다.
try { Add-BitLockerKeyProtector -MountPoint C: -TpmProtector -ErrorAction Stop | Out-Null; "  TPM protector added" } catch { "  TPM protector failed: " + $_.Exception.Message.Split('(')[0].Trim() }
$rp = Add-BitLockerKeyProtector -MountPoint C: -RecoveryPasswordProtector -WarningAction SilentlyContinue
$pw = ($rp.KeyProtector | Where-Object KeyProtectorType -eq 'RecoveryPassword').RecoveryPassword
"  recovery password shape (digits masked): " + ($pw -replace '\d', '#')
try { Resume-BitLocker -MountPoint C: -ErrorAction Stop | Out-Null } catch { "  resume failed: " + $_.Exception.Message.Split('(')[0].Trim() }
Run

"## 4. Suspend protection once (Suspend-BitLocker -RebootCount 1)"
Suspend-BitLocker -MountPoint C: -RebootCount 1 | Out-Null
Run

"## 5. Resume again"
Resume-BitLocker -MountPoint C: | Out-Null
Run
(Get-BitLockerVolume C:).KeyProtector | ForEach-Object { "  protector: " + $_.KeyProtectorType }
