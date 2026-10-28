# Harmless Microsoft Defender detection test with the standard EICAR test string.
# Run it only in a disposable test VM or on a PC you own. The test file is removed at the end.
# Usage (elevated PowerShell):
#   powershell -NoProfile -ExecutionPolicy Bypass -File .\Check-DefenderEicar.ps1 [-WaitSeconds 20]
param([int]$WaitSeconds = 20)

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$dir  = "C:\lab\eicar"
$file = Join-Path $dir "eicar-test.txt"
# The test string is split in two so that this script file itself is not flagged.
$part1 = 'X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS'
$part2 = '-TEST-FILE!$H+H*'

$st = Get-MpComputerStatus
Write-Output "== Defender status"
Write-Output ("  Real-time protection : {0}" -f $st.RealTimeProtectionEnabled)
Write-Output ("  Antivirus enabled    : {0}" -f $st.AntivirusEnabled)
Write-Output ("  Signature version    : {0}" -f $st.AntivirusSignatureVersion)

New-Item -ItemType Directory -Path $dir -Force | Out-Null
$before = @(Get-MpThreatDetection -ErrorAction SilentlyContinue).Count

$blocked = $false
try {
    Set-Content -Path $file -Value ($part1 + $part2) -NoNewline -Encoding Ascii -ErrorAction Stop
} catch {
    $blocked = $true
}

$deadline = (Get-Date).AddSeconds($WaitSeconds)
while (-not $blocked -and (Test-Path $file) -and (Get-Date) -lt $deadline) { Start-Sleep -Seconds 1 }

$stillThere = Test-Path $file
$after = @(Get-MpThreatDetection -ErrorAction SilentlyContinue).Count

Write-Output ""
Write-Output "== Test result"
Write-Output ("  Test file still exists : {0}" -f $stillThere)
Write-Output ("  New detections logged  : {0}" -f ($after - $before))

if ($stillThere) { Remove-Item $file -Force; Write-Output "  Removed the test file by hand." }
Remove-Item $dir -Force -ErrorAction SilentlyContinue

Write-Output ""
if ($stillThere -or ($after - $before) -eq 0) {
    Write-Output "Verdict: NOT DETECTED. Defender did not act on the EICAR test file."
} else {
    Write-Output "Verdict: DETECTED. Defender removed the EICAR test file and logged it."
}
