# Read-only check of disk encryption, TPM and Secure Boot. It changes nothing.
# Usage (elevated PowerShell):
#   powershell -NoProfile -ExecutionPolicy Bypass -File .\Get-BootProtection.ps1

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

function Show($name, $value, $verdict) {
    Write-Output ("  {0,-26} {1,-24} {2}" -f $name, $value, $verdict)
}

Write-Output "== BitLocker (per volume)"
try {
    foreach ($v in Get-BitLockerVolume -ErrorAction Stop) {
        $types = ($v.KeyProtector.KeyProtectorType) -join ','
        if (-not $types) { $types = 'none' }
        $verdict = if ($v.ProtectionStatus -eq 'On') { 'OK' } else { 'REVIEW: not protected' }
        Show ("{0} {1}" -f $v.MountPoint, $v.VolumeType) ("{0}/{1}" -f $v.VolumeStatus, $v.ProtectionStatus) $verdict
        Show "  key protectors" $types ''
    }
} catch {
    Show 'BitLocker' 'unreadable' $_.Exception.Message
}

Write-Output "== TPM"
try {
    $tpm = Get-Tpm -ErrorAction Stop
    Show 'present'  $tpm.TpmPresent  $(if ($tpm.TpmPresent) { 'OK' } else { 'REVIEW' })
    Show 'ready'    $tpm.TpmReady    $(if ($tpm.TpmReady) { 'OK' } else { 'REVIEW' })
    Show 'version'  $tpm.ManufacturerVersion ''
} catch {
    Show 'TPM' 'unreadable' $_.Exception.Message
}

Write-Output "== Secure Boot"
try {
    $sb = Confirm-SecureBootUEFI -ErrorAction Stop
    Show 'enabled' $sb $(if ($sb) { 'OK' } else { 'REVIEW: off' })
} catch {
    Show 'Secure Boot' 'unreadable' 'legacy BIOS or not supported'
}
