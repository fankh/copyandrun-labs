# Read-only list of logons that were given special privileges (Security event 4672). It changes nothing.
# Each 4672 is matched to the 4624 with the same logon ID to show the logon type.
# Usage (elevated PowerShell):
#   powershell -NoProfile -ExecutionPolicy Bypass -File .\Get-PrivilegedLogons.ps1 -Hours 24 [-IncludeSystem]
param([int]$Hours = 24, [switch]$IncludeSystem)

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$noise = 'SYSTEM', 'LOCAL SERVICE', 'NETWORK SERVICE'
$strong = 'SeDebugPrivilege', 'SeTcbPrivilege', 'SeLoadDriverPrivilege', 'SeBackupPrivilege',
          'SeRestorePrivilege', 'SeTakeOwnershipPrivilege', 'SeImpersonatePrivilege'

function Read-Data($e) {
    $d = @{}
    ([xml]$e.ToXml()).Event.EventData.Data | ForEach-Object { $d[$_.Name] = $_.'#text' }
    return $d
}

$start = (Get-Date).AddHours(-$Hours)
$p4672 = @(Get-WinEvent -FilterHashtable @{ LogName = 'Security'; Id = 4672; StartTime = $start } -ErrorAction SilentlyContinue)
$p4624 = @{}
foreach ($e in @(Get-WinEvent -FilterHashtable @{ LogName = 'Security'; Id = 4624; StartTime = $start } -ErrorAction SilentlyContinue)) {
    $d = Read-Data $e
    $p4624[$d.TargetLogonId] = $d
}

$rows = foreach ($e in $p4672) {
    $d = Read-Data $e
    $user = $d.SubjectUserName
    $isNoise = ($noise -contains $user) -or ($user -like 'DWM-*') -or ($user -like 'UMFD-*')
    if (-not $IncludeSystem -and $isNoise) { continue }
    $privs = @(($d.PrivilegeList -split '\s+') | Where-Object { $_ })
    $hit = @($privs | Where-Object { $strong -contains $_ })
    $logon = $p4624[$d.SubjectLogonId]
    [pscustomobject]@{
        Time      = $e.TimeCreated.ToString('MM-dd HH:mm:ss')
        User      = $user
        LogonType = if ($logon) { $logon.LogonType } else { '?' }
        Count     = $privs.Count
        Strong    = ($hit -replace '^Se', '' -replace 'Privilege$', '') -join ','
    }
}
$rows = @($rows)

Write-Output ("== Window: last {0} h, 4672 events read: {1}, shown: {2}" -f $Hours, $p4672.Count, $rows.Count)
$rows | Group-Object User | Sort-Object Count -Descending |
    ForEach-Object { Write-Output ("  {0,4}  {1}" -f $_.Count, $_.Name) }
Write-Output "== Latest 8"
$rows | Select-Object -First 8 | Format-Table -AutoSize | Out-String -Width 200 | Write-Output
