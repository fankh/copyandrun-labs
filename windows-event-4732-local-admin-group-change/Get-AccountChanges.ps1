# Read-only report of local account and group changes (Security events 4720, 4726, 4732, 4733).
# It changes nothing and does not print who made the change.
# Usage (elevated PowerShell):
#   powershell -NoProfile -ExecutionPolicy Bypass -File .\Get-AccountChanges.ps1 -Minutes 60
param([int]$Minutes = 60)

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# Subcategory GUIDs work on every display language.
$subs = [ordered]@{
    "User account management"   = '{0CCE9235-69AE-11D9-BED3-505054503030}'
    "Security group management" = '{0CCE9237-69AE-11D9-BED3-505054503030}'
}
Write-Output "== Audit settings"
$off = 0
foreach ($name in $subs.Keys) {
    $guid = $subs[$name]
    $setting = (auditpol /get /subcategory:$guid /r | ConvertFrom-Csv).'Inclusion Setting'
    if ($setting -notmatch 'Success') { $off++ }
    Write-Output ("  {0,-26}: {1}" -f $name, $setting)
}

function Resolve-Member($sid) {
    try {
        $account = (New-Object System.Security.Principal.SecurityIdentifier $sid).Translate([System.Security.Principal.NTAccount]).Value
        return ($account -split '\\')[-1]
    } catch {
        return "(deleted) RID " + ($sid -split '-')[-1]
    }
}

$kinds = @{ 4720 = "Account created"; 4726 = "Account deleted"; 4732 = "Added to group"; 4733 = "Removed from group" }
$start = (Get-Date).AddMinutes(-$Minutes)
try {
    $events = @(Get-WinEvent -FilterHashtable @{ LogName = "Security"; Id = 4720, 4726, 4732, 4733; StartTime = $start } -ErrorAction Stop)
} catch {
    $events = @()
}

$rows = foreach ($ev in $events) {
    $x = [xml]$ev.ToXml(); $d = @{}
    foreach ($n in $x.Event.EventData.Data) { $d[$n.Name] = $n.'#text' }
    $isGroup = $ev.Id -in 4732, 4733
    [pscustomobject]@{
        Time   = $ev.TimeCreated
        Kind   = $kinds[[int]$ev.Id]
        Target = $(if ($isGroup) { Resolve-Member $d.MemberSid } else { $d.TargetUserName })
        Group  = $(if ($isGroup) { $d.TargetUserName } else { "" })
        IsAdmin = ($isGroup -and $d.TargetSid -eq "S-1-5-32-544")
    }
}
$rows = @($rows | Sort-Object Time)

Write-Output ""
Write-Output ("== Account and group events in the last {0} minutes: {1}" -f $Minutes, $rows.Count)
foreach ($r in $rows) {
    Write-Output ("  {0}  {1,-19} {2,-10} {3}" -f $r.Time.ToString("HH:mm:ss"), $r.Kind, $r.Target, $r.Group)
}

$adminAdds = @($rows | Where-Object { $_.IsAdmin -and $_.Kind -eq "Added to group" }).Count

Write-Output ""
if ($off -gt 0 -and $rows.Count -eq 0) {
    Write-Output "Verdict: AUDIT OFF. Account and group changes are not recorded, so this report cannot be trusted."
} elseif ($adminAdds -gt 0) {
    Write-Output "Verdict: ALERT. $adminAdds account(s) were added to the local Administrators group. Confirm each one was expected."
} elseif ($rows.Count -eq 0) {
    Write-Output "Verdict: NO EVENTS. Auditing is on, but nothing changed in the last $Minutes minutes."
} else {
    Write-Output "Verdict: OK. Changes were recorded and none of them touched the local Administrators group."
}
