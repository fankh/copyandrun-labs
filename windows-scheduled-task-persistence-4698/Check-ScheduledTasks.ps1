# Read-only check of scheduled tasks outside \Microsoft\ and of task events 4698/4699/4702. It changes nothing.
# Usage (elevated PowerShell):
#   powershell -NoProfile -ExecutionPolicy Bypass -File .\Check-ScheduledTasks.ps1 -Minutes 60 -Known "OneDrive,MicrosoftEdgeUpdate" [-ShowRaw]
# -Known is a comma separated list of task name parts you already reviewed. Those tasks are only counted, not listed.
param([int]$Minutes = 60, [string]$Known = "", [switch]$ShowRaw)

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# The GUID of the "Other Object Access Events" subcategory works on every display language.
$guid  = '{0CCE9227-69AE-11D9-BED3-505054503030}'
$audit = (auditpol /get /subcategory:$guid /r | ConvertFrom-Csv).'Inclusion Setting'
$auditOn = [bool]($audit -match 'Success')

Write-Output "== Audit"
Write-Output ("  Other Object Access Events (4698/4699/4702) : {0}" -f $audit)

$all = @(Get-ScheduledTask | Where-Object { $_.TaskPath -notlike '\Microsoft\*' })
$knownPattern = ($Known -split ',' | Where-Object { $_.Trim() } | ForEach-Object { [regex]::Escape($_.Trim()) }) -join '|'
if ($knownPattern) {
    $tasks = @($all | Where-Object { $_.TaskName -notmatch $knownPattern })
} else {
    $tasks = $all
}
Write-Output ""
Write-Output ("== Scheduled tasks outside \Microsoft\ : {0} total, {1} already known, {2} to review" -f $all.Count, ($all.Count - $tasks.Count), $tasks.Count)
foreach ($t in $tasks) {
    $trigger = ($t.Triggers | ForEach-Object { $_.CimClass.CimClassName -replace '^MSFT_Task', '' -replace 'Trigger$', '' }) -join ','
    $action  = ($t.Actions  | ForEach-Object { ("{0} {1}" -f $_.Execute, $_.Arguments).Trim() }) -join ' ; '
    Write-Output ("  {0}{1}  [{2}]  trigger={3}  run level={4}" -f $t.TaskPath, $t.TaskName, $t.State, $trigger, $t.Principal.RunLevel)
    Write-Output ("      action: {0}" -f $action)
    if ($ShowRaw) { Write-Output ("      run as: {0}" -f $t.Principal.UserId) }
}

$start = (Get-Date).AddMinutes(-$Minutes)
try {
    $events = @(Get-WinEvent -FilterHashtable @{ LogName = 'Security'; Id = 4698, 4699, 4702; StartTime = $start } -ErrorAction Stop)
} catch {
    $events = @()
}
$names = @{ 4698 = 'created'; 4699 = 'deleted'; 4702 = 'updated' }

Write-Output ""
Write-Output ("== Task events in the last {0} minutes: {1}" -f $Minutes, $events.Count)
$events | Sort-Object TimeCreated | ForEach-Object {
    $x = [xml]$_.ToXml(); $d = @{}
    foreach ($n in $x.Event.EventData.Data) { $d[$n.Name] = $n.'#text' }
    $who = if ($ShowRaw) { $d.SubjectUserName } else { '(hidden)' }
    Write-Output ("  {0}  {1} {2,-8} {3}  by {4}" -f $_.TimeCreated.ToString("HH:mm:ss"), $_.Id, $names[$_.Id], $d.TaskName, $who)
}

Write-Output ""
if (-not $auditOn) {
    Write-Output ("Verdict: AUDIT OFF. {0} task(s) to review exist outside \Microsoft\, but their creation is not recorded." -f $tasks.Count)
} elseif ($events.Count -eq 0) {
    Write-Output "Verdict: NO EVENTS. Auditing is on, but no task was created, changed or deleted in the last $Minutes minutes."
} else {
    Write-Output "Verdict: OK. Task creation, change and deletion are recorded."
}
