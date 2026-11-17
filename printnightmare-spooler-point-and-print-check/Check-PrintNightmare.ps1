# Usage: powershell -NoProfile -File .\Check-PrintNightmare.ps1 [-Demo]
# Read only. It does not change the registry or any service.
#   - Print Spooler service status and start type
#   - Two Point and Print policy values. The CVE-2021-34527 text says 0 or not defined is the safe setting.
#   -Demo feeds the verdict function with sample values 0, 1, 2 and not defined, to show all four outputs.
# The file is ASCII only on purpose: Windows PowerShell 5.1 reads UTF-8 files without a BOM as ANSI.
param([switch]$Demo)

function Get-PolicyVerdict([string]$Name, $Value) {
    if ($null -eq $Value) { return "$Name = not defined (safe)" }
    if ($Value -eq 0) { return "$Name = 0 (safe)" }
    return "$Name = $Value (UNSAFE: set it back to 0)"
}

if ($Demo) {
    "Sample values for the verdict function"
    Get-PolicyVerdict 'NoWarningNoElevationOnInstall' 0
    Get-PolicyVerdict 'NoWarningNoElevationOnInstall' 1
    Get-PolicyVerdict 'UpdatePromptSettings' 2
    Get-PolicyVerdict 'UpdatePromptSettings' $null
    return
}

$svc = Get-Service -Name Spooler
"Print Spooler service: status $($svc.Status), start type $($svc.StartType)"

$key = 'HKLM:\SOFTWARE\Policies\Microsoft\Windows NT\Printers\PointAndPrint'
foreach ($name in 'NoWarningNoElevationOnInstall', 'UpdatePromptSettings') {
    $value = $null
    if (Test-Path $key) {
        $value = (Get-ItemProperty -Path $key -Name $name -ErrorAction SilentlyContinue).$name
    }
    Get-PolicyVerdict $name $value
}
