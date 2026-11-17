# Read-only check of PowerShell script block logging (event 4104). It changes nothing.
# Usage (elevated PowerShell):
#   powershell -NoProfile -ExecutionPolicy Bypass -File .\Check-ScriptBlockLogging.ps1 -Minutes 30 -Match "Get-Date,whoami" [-ShowRaw]
param([int]$Minutes = 30, [string]$Match = "", [int]$Last = 8, [switch]$ShowRaw)

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$key    = 'HKLM:\SOFTWARE\Policies\Microsoft\Windows\PowerShell\ScriptBlockLogging'
$value  = (Get-ItemProperty $key -ErrorAction SilentlyContinue).EnableScriptBlockLogging
$policy = switch ($value) { 1 { 'Enabled' } 0 { 'Disabled' } default { 'Not configured' } }

$logName = 'Microsoft-Windows-PowerShell/Operational'
$log     = Get-WinEvent -ListLog $logName

Write-Output "== Settings"
Write-Output ("  Script block logging policy : {0}" -f $policy)
Write-Output ("  Log {0} : {1} MB max, {2} MB used" -f $logName, [math]::Round($log.MaximumSizeInBytes / 1MB), [math]::Round($log.FileSize / 1MB, 1))

$start = (Get-Date).AddMinutes(-$Minutes)
try {
    $events = @(Get-WinEvent -FilterHashtable @{ LogName = $logName; Id = 4104; StartTime = $start } -ErrorAction Stop)
} catch {
    $events = @()
}

function Redact($text) {
    if ($ShowRaw -or [string]::IsNullOrEmpty($text)) { return $text }
    $text = $text -replace '(?i)(pass(word)?\s*[=:]\s*)\S+', '$1***'
    return ($text -replace '(?i)(ConvertTo-SecureString\s+(-String\s+)?)([''"]).*?\3', '$1***')
}

# Skip the blocks that belong to this script and to the command line that starts it.
$rows = foreach ($ev in $events) {
    $path = [string]$ev.Properties[4].Value
    $text = ([string]$ev.Properties[2].Value).Trim() -replace '\s+', ' '
    if ($path -like '*Check-ScriptBlockLogging.ps1' -or $text -match 'Check-ScriptBlockLogging') { continue }
    [pscustomobject]@{
        Time  = $ev.TimeCreated.ToString("HH:mm:ss")
        Level = $ev.LevelDisplayName
        Text  = Redact $text
    }
}
if ($Match) {
    $pattern = ($Match -split "," | ForEach-Object { [regex]::Escape($_.Trim()) }) -join "|"
    $rows = @($rows | Where-Object { $_.Text -match $pattern })
}
$rows = @($rows)

Write-Output ""
Write-Output ("== Script block events (4104) in the last {0} minutes: {1}" -f $Minutes, $rows.Count)
$rows | Sort-Object Time | Select-Object -Last $Last | ForEach-Object {
    $t = if ($_.Text.Length -gt 70) { $_.Text.Substring(0, 70) + '...' } else { $_.Text }
    Write-Output ("  {0}  {1,-11} {2}" -f $_.Time, $_.Level, $t)
}

Write-Output ""
if ($policy -ne 'Enabled') {
    Write-Output "Verdict: LOGGING OFF. Script contents are not recorded (only blocks PowerShell itself flags as suspicious)."
} elseif ($rows.Count -eq 0) {
    Write-Output "Verdict: NO EVENTS. Logging is on, but nothing matched in the last $Minutes minutes."
} else {
    Write-Output "Verdict: OK. Script block contents are recorded."
}
