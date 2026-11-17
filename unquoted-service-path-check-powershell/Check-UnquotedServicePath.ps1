# Usage: powershell -NoProfile -File .\Check-UnquotedServicePath.ps1 [-Demo] [-ShowNames]
# Read only. It lists nothing about your services unless you pass -ShowNames.
# A service path is flagged when it is not quoted and the executable part (up to .exe) contains a space.
#   -Demo feeds the judge function with four sample paths.
# The file is ASCII only on purpose: Windows PowerShell 5.1 reads UTF-8 files without a BOM as ANSI.
param([switch]$Demo, [switch]$ShowNames)

function Test-UnquotedPath([string]$Path) {
    if ([string]::IsNullOrWhiteSpace($Path)) { return $false }
    $p = $Path.Trim()
    if ($p.StartsWith('"')) { return $false }
    $m = [regex]::Match($p, '^(.*?\.exe)', 'IgnoreCase')
    if (-not $m.Success) { return $false }
    return $m.Groups[1].Value.Contains(' ')
}

if ($Demo) {
    $samples = @(
        'C:\Program Files\Vendor App\svc.exe -k run',
        '"C:\Program Files\Vendor App\svc.exe" -k run',
        'C:\Tools\svc.exe /s',
        'C:\Windows\System32\svchost.exe -k netsvcs'
    )
    foreach ($s in $samples) {
        $flag = if (Test-UnquotedPath $s) { 'FLAGGED' } else { 'ok     ' }
        "$flag  $s"
    }
    return
}

$services = Get-CimInstance Win32_Service
$flagged = $services | Where-Object { Test-UnquotedPath $_.PathName }
"Services checked: $($services.Count)"
"Flagged (unquoted path with a space): $(@($flagged).Count)"
if ($ShowNames) {
    $flagged | ForEach-Object { "  $($_.Name)  $($_.PathName)" }
}
