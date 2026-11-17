# Read-only check of SMB hardening (SMB1, signing, encryption, shares, audit). It changes nothing.
# Usage (elevated PowerShell):
#   powershell -NoProfile -ExecutionPolicy Bypass -File .\Get-SmbHardening.ps1

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

function Show($name, $value, $verdict) {
    Write-Output ("  {0,-34} {1,-10} {2}" -f $name, $value, $verdict)
}
function Flag($ok, $bad) { if ($ok) { 'OK' } else { $bad } }

$srv = Get-SmbServerConfiguration
$cli = Get-SmbClientConfiguration

Write-Output "== SMB1"
Show 'Server EnableSMB1Protocol' $srv.EnableSMB1Protocol (Flag (-not $srv.EnableSMB1Protocol) 'REVIEW: SMB1 on')
foreach ($f in Get-WindowsOptionalFeature -Online | Where-Object FeatureName -like 'SMB1Protocol*' | Sort-Object FeatureName) {
    Show ("Feature " + $f.FeatureName) $f.State (Flag ($f.State -eq 'Disabled') 'REVIEW')
}

Write-Output "== Signing and encryption"
Show 'Server RequireSecuritySignature' $srv.RequireSecuritySignature (Flag $srv.RequireSecuritySignature 'REVIEW: not required')
Show 'Client RequireSecuritySignature' $cli.RequireSecuritySignature (Flag $cli.RequireSecuritySignature 'REVIEW: not required')
Show 'Server EncryptData' $srv.EncryptData (Flag $srv.EncryptData 'info: shares not forced to encrypt')
Show 'Server RejectUnencryptedAccess' $srv.RejectUnencryptedAccess (Flag $srv.RejectUnencryptedAccess 'REVIEW')

Write-Output "== Shares"
foreach ($s in Get-SmbShare) {
    $kind = if ($s.Special) { 'built-in' } else { 'USER SHARE' }
    Show $s.Name $kind $(if ($s.Special) { '' } else { 'REVIEW: who can open it' })
}
$conn = @(Get-SmbConnection -ErrorAction SilentlyContinue)
Show 'Open client connections' $conn.Count ''

Write-Output "== Audit (who opened a share, events 5140 and 5145)"
$share = (auditpol /get /subcategory:"File Share" /r | ConvertFrom-Csv).'Inclusion Setting'
Show 'File Share audit' $share (Flag ($share -match 'Success') 'REVIEW: share access not recorded')
