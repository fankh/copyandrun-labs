# Read-only analysis of failed logons (Security event 4625). It changes nothing.
# Usage (elevated PowerShell):
#   powershell -NoProfile -ExecutionPolicy Bypass -File .\Get-FailedLogons.ps1 -Minutes 60 [-ShowAccounts]
param([int]$Minutes = 10080, [switch]$ShowAccounts)

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$logonTypes = @{ "2"="Interactive (local)"; "3"="Network"; "5"="Service"; "7"="Unlock"; "8"="NetworkCleartext"; "10"="RemoteInteractive (RDP)" }
$subStatus  = @{ "0xc000006a"="Wrong password"; "0xc0000064"="User does not exist"; "0xc000006d"="Bad user name or auth info";
                 "0xc0000234"="Account locked out"; "0xc0000072"="Account disabled" }

function Mask($name) {
    if ($ShowAccounts -or [string]::IsNullOrEmpty($name)) { return $name }
    return ($name.Substring(0, 1) + "***")
}

$start = (Get-Date).AddMinutes(-$Minutes)
try {
    $events = Get-WinEvent -FilterHashtable @{ LogName = "Security"; Id = 4625; StartTime = $start } -ErrorAction Stop
} catch {
    if ($_.Exception.Message -like "*No events were found*") { Write-Output "No 4625 events in the last $Minutes minutes."; exit 0 }
    Write-Output "Cannot read the Security log. Run in an elevated PowerShell."; exit 1
}

$rows = foreach ($ev in $events) {
    $x = [xml]$ev.ToXml(); $d = @{}
    foreach ($n in $x.Event.EventData.Data) { $d[$n.Name] = $n.'#text' }
    $sub = "$($d.SubStatus)".ToLower()
    [pscustomobject]@{
        Time    = $ev.TimeCreated
        User    = $d.TargetUserName
        Type    = $d.LogonType
        TypeTxt = $(if ($logonTypes[$d.LogonType]) { $logonTypes[$d.LogonType] } else { "Type $($d.LogonType)" })
        Reason  = $(if ($subStatus[$sub]) { $subStatus[$sub] } else { $sub })
        Ip      = $(if ($d.IpAddress -and $d.IpAddress -ne "-") { $d.IpAddress } else { "(none)" })
        Process = $(if ($d.ProcessName -and $d.ProcessName -ne "-") { Split-Path $d.ProcessName -Leaf } else { "(none)" })
    }
}

$total   = @($rows).Count
$remote  = @($rows | Where-Object { $_.Type -in @("3", "8", "10") }).Count
$ips     = @($rows | Where-Object { $_.Ip -ne "(none)" } | Select-Object -ExpandProperty Ip -Unique).Count
$users   = @($rows | Select-Object -ExpandProperty User -Unique).Count
$locked  = @($rows | Where-Object { $_.Reason -eq "Account locked out" }).Count
$unknown = @($rows | Where-Object { $_.Reason -in @("User does not exist", "Bad user name or auth info") }).Count

$byType = $rows | Group-Object TypeTxt | Sort-Object Count -Descending
$byWhy  = $rows | Group-Object Reason | Sort-Object Count -Descending
$byUser = $rows | Group-Object User | Sort-Object Count -Descending | Select-Object -First 5
$byProc = $rows | Group-Object Process | Sort-Object Count -Descending | Select-Object -First 5
$byIp   = $rows | Group-Object Ip | Sort-Object Count -Descending | Select-Object -First 5

$signals = New-Object System.Collections.Generic.List[string]
if ($remote -gt 0)  { $signals.Add("REMOTE: $remote failures came over the network or RDP (type 3, 8, 10).") }
if ($ips -ge 1)     { $signals.Add("SOURCES: $ips distinct source IP address(es) appear in the events.") }
if ($users -ge 5)   { $signals.Add("SPRAY: $users different account names were tried.") }
if ($unknown -gt 0) { $signals.Add("GUESSING: $unknown failures used names that do not exist.") }
if ($locked -gt 0)  { $signals.Add("LOCKOUT: $locked failures hit a locked account.") }
$verdict = if ($remote -gt 0 -or $ips -ge 1 -or $users -ge 5 -or $unknown -gt 0) { "REVIEW: signs of remote or guessing activity" }
           else { "LOCAL ONLY: no remote source, one or few accounts, known account names" }

function Show($title, $groups, [bool]$maskKey = $false) {
    Write-Output ""; Write-Output "== $title"
    foreach ($g in $groups) {
        $k = if ($maskKey) { Mask $g.Name } else { $g.Name }
        Write-Output ("{0,6}  {1}" -f $g.Count, $k)
    }
}

Write-Output "Failed logons (4625) in the last $Minutes minutes: $total"
Show "By logon type" $byType
Show "By reason" $byWhy
Show "By account" $byUser $true
Show "By source IP" $byIp
Show "By process" $byProc
Write-Output ""
Write-Output "== Signals"
if ($signals.Count -eq 0) { Write-Output "  (none)" } else { $signals | ForEach-Object { Write-Output "  $_" } }
Write-Output ""
Write-Output "Verdict: $verdict"
