# Read-only summary of successful logons (Security event 4624). It changes nothing.
# Usage (elevated PowerShell):
#   powershell -NoProfile -ExecutionPolicy Bypass -File .\Get-LogonSummary.ps1 -Hours 24 [-User name] [-IncludeService]
param([int]$Hours = 24, [string]$User = "", [switch]$IncludeService)

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$typeName = @{
    0  = 'System'
    2  = 'Interactive (console or runas)'
    3  = 'Network (SMB, WinRM, net use)'
    4  = 'Batch (scheduled task)'
    5  = 'Service'
    7  = 'Unlock'
    8  = 'NetworkCleartext'
    9  = 'NewCredentials (runas /netonly)'
    10 = 'RemoteInteractive (RDP)'
    11 = 'CachedInteractive'
}
$noise = 'SYSTEM', 'LOCAL SERVICE', 'NETWORK SERVICE', 'ANONYMOUS LOGON'

$start = (Get-Date).AddHours(-$Hours)
try {
    $events = @(Get-WinEvent -FilterHashtable @{ LogName = 'Security'; Id = 4624; StartTime = $start } -ErrorAction Stop)
} catch {
    $events = @()
}

$rows = foreach ($e in $events) {
    $d = @{}
    ([xml]$e.ToXml()).Event.EventData.Data | ForEach-Object { $d[$_.Name] = $_.'#text' }
    $t = [int]$d.LogonType
    $isNoise = ($noise -contains $d.TargetUserName) -or ($d.TargetUserName -like 'DWM-*') -or ($d.TargetUserName -like 'UMFD-*')
    if (-not $IncludeService -and ($isNoise -or $t -eq 5)) { continue }
    if ($User -and $d.TargetUserName -ne $User) { continue }
    $ip = $d.IpAddress
    $remote = ($ip -and $ip -notin @('-', '::1', '127.0.0.1'))
    [pscustomobject]@{
        Time    = $e.TimeCreated.ToString('MM-dd HH:mm:ss')
        Type    = $t
        Meaning = $typeName[$t]
        User    = $d.TargetUserName
        Process = if ($d.ProcessName -and $d.ProcessName -ne '-') { Split-Path $d.ProcessName -Leaf } else { '-' }
        Auth    = $d.AuthenticationPackageName
        Source  = $ip
        Remote  = $remote
    }
}
$rows = @($rows)

Write-Output ("== Window: last {0} h, events read: {1}, shown: {2}" -f $Hours, $events.Count, $rows.Count)
if ($events.Count -gt 0) {
    Write-Output ("   oldest event in this window: {0}" -f $events[-1].TimeCreated.ToString('MM-dd HH:mm:ss'))
}
Write-Output "== By logon type"
$rows | Group-Object Type, Meaning | Sort-Object Count -Descending |
    ForEach-Object { Write-Output ("  {0,4}  {1}" -f $_.Count, $_.Name) }
Write-Output "== Remote sources (type 3 or 10 from a non-loopback address)"
$remote = @($rows | Where-Object { $_.Remote -and $_.Type -in 3, 10 })
if ($remote.Count -eq 0) { Write-Output "  none" } else { $remote | Format-Table Time, Type, User, Source, Auth -AutoSize }
Write-Output "== Latest 8"
$rows | Select-Object -First 8 | Format-Table Time, Type, User, Process, Auth, Source -AutoSize
