# SMB 설정을 시험용으로 바꿔 보고 Get-SmbHardening.ps1 의 결과가 어떻게 달라지는지 확인한 뒤 원래대로 돌린다.
# 주의: 시험용 PC에서만 실행한다. 공유 하나를 만들고 서명 요구, 서버 암호화, 공유 접근 감사를 바꿨다가 되돌린다.
# 준비: 같은 폴더에 Get-SmbHardening.ps1 이 있어야 한다. 관리자 PowerShell 에서 실행한다.
# 출력 문구를 영어로 쓴 이유: Windows PowerShell 5.1 은 BOM 없는 UTF-8 파일의 한글 문자열을 깨뜨려 읽을 수 있다.
# 실행: powershell -NoProfile -ExecutionPolicy Bypass -File .\Test-SmbChanges.ps1
Set-Location $PSScriptRoot
$keep = 'RequireSecuritySignature|EncryptData|File Share|Open client|ADMIN|labshare|Feature SMB1Protocol '
function Run { (powershell -NoProfile -ExecutionPolicy Bypass -File .\Get-SmbHardening.ps1) | Where-Object { $_ -match $keep } }
$dir = 'C:\' + 'labshare'

"## 1. Baseline"
Run

"## 2. Create a share, turn off server signing, turn on encryption, turn on share audit"
New-Item -ItemType Directory -Force $dir | Out-Null
Set-Content "$dir\a.txt" 'lab'
New-SmbShare -Name labshare -Path $dir -ReadAccess Everyone | Out-Null
Set-SmbServerConfiguration -RequireSecuritySignature $false -Force
Set-SmbServerConfiguration -EncryptData $true -Force
auditpol /set /subcategory:"File Share" /success:enable /failure:enable | Out-Null
Run

"## 3. Open the share, then read event 5140 from the Security log"
Get-Content "\\localhost\labshare\a.txt" | Out-Null
Start-Sleep 3
Get-WinEvent -FilterHashtable @{LogName='Security';Id=5140;StartTime=(Get-Date).AddSeconds(-20)} -MaxEvents 4 -ErrorAction SilentlyContinue | ForEach-Object {
    $d = ([xml]$_.ToXml()).Event.EventData.Data
    "{0} id {1} share {2} user {3}" -f $_.TimeCreated.ToString('HH:mm:ss'), $_.Id, ($d | Where-Object Name -eq 'ShareName').'#text', ($d | Where-Object Name -eq 'SubjectUserName').'#text'
}

"## 4. Undo everything and run again"
Remove-SmbShare -Name labshare -Force
Set-SmbServerConfiguration -RequireSecuritySignature $true -EncryptData $false -Force
auditpol /set /subcategory:"File Share" /success:disable /failure:disable | Out-Null
Get-Item $dir | Remove-Item -Recurse -Force
Run
