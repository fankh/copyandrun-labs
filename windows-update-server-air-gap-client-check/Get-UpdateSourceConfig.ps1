# Read-only check of where this PC gets Windows updates from (Microsoft, or an internal WSUS server).
# It changes nothing. For an air-gapped network the goal is: WSUS set, internet fallback blocked, server reachable.
# Usage (elevated PowerShell):
#   powershell -NoProfile -ExecutionPolicy Bypass -File .\Get-UpdateSourceConfig.ps1

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

function Show($name, $value, $verdict) {
    Write-Output ("  {0,-44} {1,-26} {2}" -f $name, $value, $verdict)
}
function Get-Policy($path, $name) {
    if (-not (Test-Path $path)) { return $null }
    return (Get-ItemProperty -Path $path -ErrorAction SilentlyContinue).$name
}

$wu = 'HKLM:\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate'
$au = 'HKLM:\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU'

$server  = Get-Policy $wu 'WUServer'
$status  = Get-Policy $wu 'WUStatusServer'
$useWsus = Get-Policy $au 'UseWUServer'
$noWeb   = Get-Policy $wu 'DoNotConnectToWindowsUpdateInternetLocations'
$noAuto  = Get-Policy $au 'NoAutoUpdate'
$options = Get-Policy $au 'AUOptions'

Write-Output "== Update source (policy)"
Show 'WUServer' $(if ($server) { $server } else { '(not set)' }) ''
Show 'WUStatusServer' $(if ($status) { $status } else { '(not set)' }) ''
Show 'UseWUServer' $(if ($null -eq $useWsus) { '(not set)' } else { $useWsus }) ''
$wsusOn = ($server -and $useWsus -eq 1)
Show 'Effective source' $(if ($wsusOn) { 'internal WSUS' } else { 'Microsoft Update' }) $(if ($wsusOn) { 'OK for air gap' } else { 'REVIEW: air gap needs an internal server' })
Show 'DoNotConnectToWindowsUpdateInternetLocations' $(if ($null -eq $noWeb) { '(not set)' } else { $noWeb }) $(if ($noWeb -eq 1) { 'OK' } else { 'REVIEW: may still try the internet' })

Write-Output "== Automatic updates (policy)"
Show 'NoAutoUpdate' $(if ($null -eq $noAuto) { '(not set)' } else { $noAuto }) $(if ($noAuto -eq 1) { 'automatic updates are off' } else { '' })
Show 'AUOptions' $(if ($null -eq $options) { '(not set)' } else { $options }) ''

Write-Output "== Reachability of the WSUS server (TCP only)"
if ($server) {
    try {
        $uri = [System.Uri]$server
        $port = if ($uri.Port -gt 0) { $uri.Port } else { 80 }
        $ok = (Test-NetConnection -ComputerName $uri.Host -Port $port -WarningAction SilentlyContinue).TcpTestSucceeded
        Show ("{0}:{1}" -f $uri.Host, $port) $ok $(if ($ok) { 'OK (port answers; not proof that WSUS works)' } else { 'REVIEW: nothing answers' })
    } catch {
        Show 'WUServer' 'not a valid URL' 'REVIEW'
    }
} else {
    Show 'WUServer' 'not set' 'skipped'
}

Write-Output "== Update services the agent knows (COM)"
$sm = New-Object -ComObject Microsoft.Update.ServiceManager
foreach ($s in $sm.Services) {
    Show $s.Name ("default={0} managed={1}" -f $s.IsDefaultAUService, $s.IsManaged) $s.ServiceUrl
}
