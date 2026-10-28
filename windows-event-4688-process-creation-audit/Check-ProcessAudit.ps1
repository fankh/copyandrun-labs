# Read-only check of process creation auditing (Security event 4688). It changes nothing.
# Usage (elevated PowerShell):
#   powershell -NoProfile -ExecutionPolicy Bypass -File .\Check-ProcessAudit.ps1 -Minutes 30 -Match "whoami,hostname,findstr" [-ShowRaw]
param([int]$Minutes = 30, [string]$Match = "", [int]$Last = 8, [switch]$ShowRaw)

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# The GUID of the "Process Creation" subcategory works on every display language.
$guid  = '{0CCE922B-69AE-11D9-BED3-505054503030}'
$audit = (auditpol /get /subcategory:$guid /r | ConvertFrom-Csv).'Inclusion Setting'
$auditOn = [bool]($audit -match 'Success')

$cmdKey = 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System\Audit'
$cmdOn  = ((Get-ItemProperty $cmdKey -ErrorAction SilentlyContinue).ProcessCreationIncludeCmdLine_Enabled -eq 1)

Write-Output "== Settings"
Write-Output ("  Process creation audit : {0}" -f $audit)
Write-Output ("  Command line included  : {0}" -f $cmdOn)

$start = (Get-Date).AddMinutes(-$Minutes)
try {
    $events = @(Get-WinEvent -FilterHashtable @{ LogName = "Security"; Id = 4688; StartTime = $start } -ErrorAction Stop)
} catch {
    $events = @()
}

function Redact($text) {
    if ($ShowRaw -or [string]::IsNullOrEmpty($text)) { return $text }
    return ($text -replace '(?i)(pass(word)?\s*[=:]\s*)\S+', '$1***')
}

$rows = foreach ($ev in $events) {
    $x = [xml]$ev.ToXml(); $d = @{}
    foreach ($n in $x.Event.EventData.Data) { $d[$n.Name] = $n.'#text' }
    [pscustomobject]@{
        Time    = $ev.TimeCreated.ToString("HH:mm:ss")
        Process = Split-Path $d.NewProcessName -Leaf
        Command = Redact $d.CommandLine
    }
}
if ($Match) {
    $pattern = ($Match -split "," | ForEach-Object { [regex]::Escape($_.Trim()) }) -join "|"
    $rows = @($rows | Where-Object { $_.Process -match $pattern })
}
$rows = @($rows)
$noCmd = @($rows | Where-Object { [string]::IsNullOrEmpty($_.Command) }).Count

Write-Output ""
Write-Output ("== Process creation events (4688) in the last {0} minutes: {1}" -f $Minutes, $rows.Count)
$rows | Sort-Object Time | Select-Object -Last $Last | ForEach-Object {
    Write-Output ("  {0}  {1,-16} {2}" -f $_.Time, $_.Process, $_.Command)
}

Write-Output ""
if (-not $auditOn) {
    Write-Output "Verdict: AUDIT OFF. Process creation is not recorded, so there is nothing to look back at."
} elseif (-not $cmdOn) {
    Write-Output "Verdict: PARTIAL. Processes are recorded, but without their command lines."
} elseif ($rows.Count -eq 0) {
    Write-Output "Verdict: NO EVENTS. Auditing is on, but nothing matched in the last $Minutes minutes."
} elseif ($noCmd -gt 0) {
    Write-Output "Verdict: CHECK. Some events have an empty command line."
} else {
    Write-Output "Verdict: OK. Processes and their command lines are recorded."
}
