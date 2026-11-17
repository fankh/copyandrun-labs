# LSA 보호와 Credential Guard 의 "설정"과 "실제 실행 상태"가 다를 수 있음을 확인한다. 레지스트리 설정을 바꾸고 재부팅 없이 두 값을 비교한 뒤 되돌린다.
# 주의: 시험용 PC에서만 실행한다. RunAsPPL 을 1로 쓰고 재부팅하면 UEFI 변수에 잠겨 되돌리기 어려워질 수 있다. 이 파일은 재부팅하지 않고 값을 원래대로 돌린다.
# 준비: 같은 폴더에 Get-LsaProtection.ps1 이 있어야 한다. 관리자 PowerShell 에서 실행한다.
# 출력 문구를 영어로 쓴 이유: Windows PowerShell 5.1 은 BOM 없는 UTF-8 파일의 한글 문자열을 깨뜨려 읽을 수 있다.
# 실행: powershell -NoProfile -ExecutionPolicy Bypass -File .\Test-LsaConfigVsRunning.ps1
Set-Location $PSScriptRoot
function Run { (powershell -NoProfile -ExecutionPolicy Bypass -File .\Get-LsaProtection.ps1) | Where-Object { $_ -match 'RunAsPPL|LsaCfgFlags|VBS|Services running|last boot|none|protected' } }
$lsa = 'HKLM:\SYSTEM\CurrentControlSet\Control\Lsa'
function Dg { Get-CimInstance -ClassName Win32_DeviceGuard -Namespace root\Microsoft\Windows\DeviceGuard -ErrorAction SilentlyContinue }

"## 1. Initial state (script)"
Run

"## 2. Raw values: registry setting and what is actually running"
$orig = (Get-ItemProperty $lsa).RunAsPPL
"  RunAsPPL = $orig"
$dg = Dg
"  VirtualizationBasedSecurityStatus = " + $dg.VirtualizationBasedSecurityStatus + " (0 means off)"
"  SecurityServicesRunning = [" + ($dg.SecurityServicesRunning -join ',') + "] (empty or 0 means nothing running)"

"## 3. Change only the settings: RunAsPPL=1 and LsaCfgFlags=1"
Set-ItemProperty $lsa -Name RunAsPPL -Value 1 -Type DWord
Set-ItemProperty $lsa -Name LsaCfgFlags -Value 1 -Type DWord
Run

"## 4. No reboot, so is the running state unchanged?"
$dg = Dg
"  VirtualizationBasedSecurityStatus = " + $dg.VirtualizationBasedSecurityStatus + ", SecurityServicesRunning = [" + ($dg.SecurityServicesRunning -join ',') + "]"

"## 5. Put the settings back"
Set-ItemProperty $lsa -Name RunAsPPL -Value $orig -Type DWord
Remove-ItemProperty $lsa -Name LsaCfgFlags -ErrorAction SilentlyContinue
Run
