# Read-only timeline of local account changes in the Security log. It changes nothing.
# 4720 created, 4722 enabled, 4724 password reset, 4725 disabled, 4726 deleted, 4740 locked out
# Usage (elevated PowerShell):
#   powershell -NoProfile -ExecutionPolicy Bypass -File .\Get-AccountChanges.ps1 -Minutes 60 [-Account name]
param([int]$Minutes = 60, [string]$Account = "")

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$meaning = @{
    4720 = 'created'
    4722 = 'enabled'
    4724 = 'password reset'
    4725 = 'disabled'
    4726 = 'deleted'
    4740 = 'locked out'
}

$start = (Get-Date).AddMinutes(-$Minutes)
try {
    $events = @(Get-WinEvent -FilterHashtable @{ LogName = 'Security'; Id = @($meaning.Keys); StartTime = $start } -ErrorAction Stop)
} catch {
    $events = @()
}

$rows = foreach ($e in $events) {
    $d = @{}
    ([xml]$e.ToXml()).Event.EventData.Data | ForEach-Object { $d[$_.Name] = $_.'#text' }
    if ($Account -and $d.TargetUserName -ne $Account) { continue }
    [pscustomobject]@{
        At      = $e.TimeCreated
        Time    = $e.TimeCreated.ToString('HH:mm:ss')
        Id      = $e.Id
        Change  = $meaning[[int]$e.Id]
        Target  = $d.TargetUserName
        By      = $d.SubjectUserName
        # 4740 puts the computer that sent the bad logons in TargetDomainName
        From    = if ($e.Id -eq 4740) { $d.TargetDomainName } else { '' }
    }
}
$rows = @($rows | Sort-Object At, Id)

Write-Output ("== Window: last {0} min, events: {1}" -f $Minutes, $rows.Count)
Write-Output "== Timeline"
$rows | Format-Table Time, Id, Change, Target, By, From -AutoSize | Out-String -Width 200 | Write-Output
$locked = @($rows | Where-Object { $_.Id -eq 4740 })
if ($locked.Count -gt 0) { Write-Output ("== Lockouts: {0} (accounts: {1})" -f $locked.Count, (($locked.Target | Sort-Object -Unique) -join ', ')) }
