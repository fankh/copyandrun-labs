# Read-only check of two persistence places: new services (event 7045) and WMI event subscriptions.
# It changes nothing.
# Usage (elevated PowerShell):
#   powershell -NoProfile -ExecutionPolicy Bypass -File .\Get-ServiceAndWmiPersistence.ps1 -Hours 24 [-Match crlab]
param([int]$Hours = 24, [string]$Match = "")

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$start = (Get-Date).AddHours(-$Hours)

Write-Output "== New services (System log, event 7045, last $Hours h)"
$new = @(Get-WinEvent -FilterHashtable @{ LogName = 'System'; ProviderName = 'Service Control Manager'; Id = 7045; StartTime = $start } -ErrorAction SilentlyContinue)
$shown = 0
foreach ($e in ($new | Sort-Object TimeCreated)) {
    $d = @{}
    ([xml]$e.ToXml()).Event.EventData.Data | ForEach-Object { $d[$_.Name] = $_.'#text' }
    if ($Match -and ($d.ServiceName -notlike "*$Match*") -and ($d.ImagePath -notlike "*$Match*")) { continue }
    $shown++
    Write-Output ("  {0}  {1}" -f $e.TimeCreated.ToString('MM-dd HH:mm:ss'), $d.ServiceName)
    Write-Output ("      image: {0}" -f $d.ImagePath)
    Write-Output ("      type: {0}, start: {1}, account: {2}" -f $d.ServiceType, $d.StartType, $d.AccountName)
}
if ($shown -eq 0) { Write-Output "  none" }

Write-Output "== Services running from outside Windows and Program Files"
$odd = @(Get-CimInstance Win32_Service | Where-Object {
    $_.PathName -and ($_.PathName -notlike '*\Windows\*') -and ($_.PathName -notlike '*Program Files*') -and ($_.PathName -notlike '*ProgramData\Microsoft*')
})
if ($Match) { $odd = @($odd | Where-Object { $_.Name -like "*$Match*" -or $_.PathName -like "*$Match*" }) }
if ($odd.Count -eq 0) { Write-Output "  none" } else { foreach ($s in $odd) { Write-Output ("  {0} [{1}/{2}]  {3}" -f $s.Name, $s.StartMode, $s.State, $s.PathName) } }

Write-Output "== WMI event subscriptions (root\subscription)"
$ns = 'root\subscription'
$filters   = @(Get-CimInstance -Namespace $ns -ClassName __EventFilter -ErrorAction SilentlyContinue)
$consumers = @(Get-CimInstance -Namespace $ns -ClassName __EventConsumer -ErrorAction SilentlyContinue)
$bindings  = @(Get-CimInstance -Namespace $ns -ClassName __FilterToConsumerBinding -ErrorAction SilentlyContinue)
if ($Match) {
    $filters   = @($filters   | Where-Object { $_.Name -like "*$Match*" -or $_.Query -like "*$Match*" })
    $consumers = @($consumers | Where-Object { $_.Name -like "*$Match*" -or ($_.PSObject.Properties['CommandLineTemplate'] -and $_.CommandLineTemplate -like "*$Match*") })
    $bindings  = @($bindings  | Where-Object { "$($_.Filter)" -like "*$Match*" -or "$($_.Consumer)" -like "*$Match*" })
}
Write-Output ("  filters: {0}, consumers: {1}, bindings: {2}" -f $filters.Count, $consumers.Count, $bindings.Count)
foreach ($f in $filters)   { Write-Output ("  filter   {0}: {1}" -f $f.Name, $f.Query) }
foreach ($c in $consumers) {
    $detail = if ($c.PSObject.Properties['CommandLineTemplate']) { $c.CommandLineTemplate } elseif ($c.PSObject.Properties['ScriptText']) { 'script text' } else { '' }
    Write-Output ("  consumer {0} [{1}] {2}" -f $c.Name, $c.CimClass.CimClassName, $detail)
}
