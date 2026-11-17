# Read-only check of LSA protection and Credential Guard. It changes nothing.
# Usage (elevated PowerShell):
#   powershell -NoProfile -ExecutionPolicy Bypass -File .\Get-LsaProtection.ps1

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

function Show($name, $value, $verdict) {
    Write-Output ("  {0,-30} {1,-14} {2}" -f $name, $value, $verdict)
}

$lsa = Get-ItemProperty 'HKLM:\SYSTEM\CurrentControlSet\Control\Lsa'
Write-Output "== Registry (configuration)"
$ppl = $lsa.RunAsPPL
$pplText = switch ($ppl) { 0 { 'off' } 1 { 'on, UEFI locked' } 2 { 'on' } default { 'not set' } }
Show 'RunAsPPL' $(if ($null -eq $ppl) { '-' } else { $ppl }) $pplText
$cg = $lsa.LsaCfgFlags
$cgText = switch ($cg) { 0 { 'off' } 1 { 'on, UEFI locked' } 2 { 'on' } default { 'not set' } }
Show 'LsaCfgFlags' $(if ($null -eq $cg) { '-' } else { $cg }) $cgText

Write-Output "== Running state (what is actually active)"
$dg = Get-CimInstance -ClassName Win32_DeviceGuard -Namespace 'root\Microsoft\Windows\DeviceGuard' -ErrorAction SilentlyContinue
if ($dg) {
    $vbs = switch ([int]$dg.VirtualizationBasedSecurityStatus) { 0 { 'off' } 1 { 'enabled, not running' } 2 { 'running' } default { 'unknown' } }
    Show 'VBS' $dg.VirtualizationBasedSecurityStatus $vbs
    $names = @{ 1 = 'Credential Guard'; 2 = 'HVCI (memory integrity)'; 3 = 'System Guard' }
    $running = @($dg.SecurityServicesRunning | ForEach-Object { $names[[int]$_] } | Where-Object { $_ })
    Show 'Services running' ($dg.SecurityServicesRunning -join ',') $(if ($running) { $running -join ', ' } else { 'none' })
} else {
    Show 'Device Guard' 'unreadable' ''
}

Write-Output "== Boot events (Wininit)"
$boot = (Get-CimInstance Win32_OperatingSystem).LastBootUpTime
Write-Output ("  last boot: {0}" -f $boot.ToString('yyyy-MM-dd HH:mm'))
$events = @(Get-WinEvent -FilterHashtable @{ LogName = 'System'; ProviderName = 'Microsoft-Windows-Wininit'; StartTime = $boot.AddMinutes(-5) } -ErrorAction SilentlyContinue |
    Where-Object { $_.Id -in 12, 14, 18 } | Sort-Object TimeCreated)
if ($events.Count -eq 0) {
    Write-Output "  none (log rolled over or protection was not started)"
} else {
    foreach ($e in $events) {
        $first = ($e.Message -split "`r?`n")[0]
        Write-Output ("  {0} id {1}: {2}" -f $e.TimeCreated.ToString('MM-dd HH:mm'), $e.Id, $first)
    }
}
