# Read-only reader for Sysmon events 1 (process create), 3 (network connect) and 11 (file create).
# It changes nothing. Add -Chain to group the events of one process by its ProcessGuid.
# Usage (elevated PowerShell):
#   powershell -NoProfile -ExecutionPolicy Bypass -File .\Get-SysmonEvents.ps1 -Minutes 10 [-Match crlab] [-Chain]
param([int]$Minutes = 10, [string]$Match = "", [switch]$Chain)

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$log = 'Microsoft-Windows-Sysmon/Operational'
$start = (Get-Date).AddMinutes(-$Minutes)
try {
    $events = @(Get-WinEvent -FilterHashtable @{ LogName = $log; Id = 1, 3, 11; StartTime = $start } -ErrorAction Stop)
} catch {
    Write-Output "Sysmon log not readable: $($_.Exception.Message)"
    return
}

$rows = foreach ($e in ($events | Sort-Object TimeCreated)) {
    $d = @{}
    ([xml]$e.ToXml()).Event.EventData.Data | ForEach-Object { $d[$_.Name] = $_.'#text' }
    $what = switch ($e.Id) {
        1  { $d.CommandLine }
        3  { "{0}:{1}" -f $d.DestinationIp, $d.DestinationPort }
        11 { $d.TargetFilename }
    }
    if ($Match -and ($what -notlike "*$Match*") -and ($d.Image -notlike "*$Match*")) { continue }
    [pscustomobject]@{
        At = $e.TimeCreated; Time = $e.TimeCreated.ToString('HH:mm:ss'); Id = $e.Id
        Image = (Split-Path $d.Image -Leaf); What = $what; Guid = $d.ProcessGuid
        Parent = if ($d.ParentImage) { Split-Path $d.ParentImage -Leaf } else { '' }
        Sha256 = if ($d.Hashes) { ($d.Hashes -replace '^SHA256=', '').Substring(0, 12) } else { '' }
    }
}
$rows = @($rows)

Write-Output ("== Window: last {0} min, events shown: {1}" -f $Minutes, $rows.Count)
if (-not $Chain) {
    foreach ($r in $rows) {
        Write-Output ("  {0}  id {1,-2} {2}" -f $r.Time, $r.Id, $r.Image)
        Write-Output ("        {0}" -f $r.What)
        if ($r.Id -eq 1) { Write-Output ("        parent: {0}  sha256: {1}..." -f $r.Parent, $r.Sha256) }
    }
} else {
    foreach ($g in ($rows | Group-Object Guid | Sort-Object { $_.Group[0].At })) {
        Write-Output ("  process {0}  ({1})" -f $g.Group[0].Image, $g.Name)
        foreach ($r in $g.Group) {
            $label = switch ($r.Id) { 1 { 'started' } 3 { 'connected' } 11 { 'created file' } }
            Write-Output ("    {0}  {1,-12} {2}" -f $r.Time, $label, $r.What)
        }
    }
}
