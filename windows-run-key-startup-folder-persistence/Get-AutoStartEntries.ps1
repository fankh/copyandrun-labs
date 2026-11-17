# Read-only list of programs that start by themselves at logon (Run keys and Startup folders).
# It changes nothing. REVIEW marks entries that run from a user-writable folder or through a script engine.
# Usage (elevated PowerShell):
#   powershell -NoProfile -ExecutionPolicy Bypass -File .\Get-AutoStartEntries.ps1 [-Match crlab]
param([string]$Match = "")

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$writable = 'AppData', '\Temp\', '\Users\Public', 'Downloads', 'ProgramData'
$engines  = 'powershell', 'pwsh', 'cmd.exe', 'wscript', 'cscript', 'mshta', 'rundll32', 'regsvr32'

function Judge($command) {
    $why = @()
    foreach ($w in $writable) { if ($command -like "*$w*") { $why += "user-writable path ($w)"; break } }
    foreach ($x in $engines)  { if ($command -like "*$x*") { $why += "script engine ($x)"; break } }
    return ($why -join '; ')
}

$keys = @(
    @{ Scope = 'HKLM'; Path = 'HKLM:\Software\Microsoft\Windows\CurrentVersion\Run' },
    @{ Scope = 'HKLM'; Path = 'HKLM:\Software\Microsoft\Windows\CurrentVersion\RunOnce' },
    @{ Scope = 'HKCU'; Path = 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Run' },
    @{ Scope = 'HKCU'; Path = 'HKCU:\Software\Microsoft\Windows\CurrentVersion\RunOnce' }
)

$rows = @()
foreach ($k in $keys) {
    if (-not (Test-Path $k.Path)) { continue }
    $props = Get-ItemProperty $k.Path
    foreach ($p in $props.PSObject.Properties) {
        if ($p.Name -like 'PS*') { continue }
        $rows += [pscustomobject]@{ Where = "$($k.Scope) " + ($k.Path -replace '.*\\', ''); Name = $p.Name; Command = [string]$p.Value; Why = (Judge ([string]$p.Value)) }
    }
}
$folders = @(
    @{ Scope = 'User Startup';   Path = [Environment]::GetFolderPath('Startup') },
    @{ Scope = 'Common Startup'; Path = [Environment]::GetFolderPath('CommonStartup') }
)
foreach ($f in $folders) {
    if (-not (Test-Path $f.Path)) { continue }
    foreach ($i in Get-ChildItem $f.Path -File -Force -ErrorAction SilentlyContinue | Where-Object Name -ne 'desktop.ini') {
        $rows += [pscustomobject]@{ Where = $f.Scope; Name = $i.Name; Command = $i.FullName; Why = (Judge $i.FullName) }
    }
}
if ($Match) { $rows = @($rows | Where-Object { $_.Name -like "*$Match*" -or $_.Command -like "*$Match*" }) }

Write-Output ("== Entries: {0}, REVIEW: {1}" -f $rows.Count, @($rows | Where-Object Why).Count)
foreach ($r in $rows) {
    Write-Output ("  [{0}] {1}" -f $r.Where, $r.Name)
    Write-Output ("      {0}" -f $r.Command)
    if ($r.Why) { Write-Output ("      REVIEW: {0}" -f $r.Why) }
}
