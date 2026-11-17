# Read-only check of SMB shares (without the built-in admin shares) and of share access events 5140/5145. It changes nothing.
# Usage (elevated PowerShell):
#   powershell -NoProfile -ExecutionPolicy Bypass -File .\Check-SmbShares.ps1 -Minutes 30 [-ShowRaw]
param([int]$Minutes = 30, [int]$Last = 8, [switch]$ShowRaw)

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# The GUIDs of the "File Share" and "Detailed File Share" subcategories work on every display language.
$share  = (auditpol /get /subcategory:'{0CCE9224-69AE-11D9-BED3-505054503030}' /r | ConvertFrom-Csv).'Inclusion Setting'
$detail = (auditpol /get /subcategory:'{0CCE9244-69AE-11D9-BED3-505054503030}' /r | ConvertFrom-Csv).'Inclusion Setting'
$auditOn = [bool]($share -match 'Success')

Write-Output "== Audit"
Write-Output ("  File Share          (5140)       : {0}" -f $share)
Write-Output ("  Detailed File Share (5145)       : {0}" -f $detail)

$shares = @(Get-SmbShare | Where-Object { -not $_.Special })
Write-Output ""
Write-Output ("== Shares besides the admin shares: {0}" -f $shares.Count)
foreach ($s in $shares) {
    $access = (Get-SmbShareAccess -Name $s.Name | ForEach-Object { "{0}:{1}" -f $_.AccountName, $_.AccessRight }) -join ', '
    Write-Output ("  {0}  path={1}" -f $s.Name, $s.Path)
    Write-Output ("      access: {0}" -f $access)
}

$start = (Get-Date).AddMinutes(-$Minutes)
try {
    $events = @(Get-WinEvent -FilterHashtable @{ LogName = 'Security'; Id = 5140, 5145; StartTime = $start } -ErrorAction Stop)
} catch {
    $events = @()
}

$rows = foreach ($ev in $events) {
    $x = [xml]$ev.ToXml(); $d = @{}
    foreach ($n in $x.Event.EventData.Data) { $d[$n.Name] = $n.'#text' }
    if ($d.ShareName -match '\$$') { continue }   # skip IPC$ and the other admin shares
    [pscustomobject]@{
        Time   = $ev.TimeCreated
        Id     = $ev.Id
        Share  = $d.ShareName
        Target = $d.RelativeTargetName
        From   = $d.IpAddress
        By     = if ($ShowRaw) { $d.SubjectUserName } else { '(hidden)' }
    }
}
$rows = @($rows)

Write-Output ""
Write-Output ("== Share access events in the last {0} minutes (admin shares skipped): {1}" -f $Minutes, $rows.Count)
$rows | Sort-Object Time | Select-Object -Last $Last | ForEach-Object {
    Write-Output ("  {0}  {1}  {2,-12} {3,-12} from {4}  by {5}" -f $_.Time.ToString("HH:mm:ss"), $_.Id, $_.Share, $_.Target, $_.From, $_.By)
}

Write-Output ""
if (-not $auditOn) {
    Write-Output ("Verdict: AUDIT OFF. {0} share(s) exist, but access to them is not recorded." -f $shares.Count)
} elseif ($rows.Count -eq 0) {
    Write-Output "Verdict: NO EVENTS. Auditing is on, but no share was accessed in the last $Minutes minutes."
} else {
    Write-Output "Verdict: OK. Share access is recorded."
}
