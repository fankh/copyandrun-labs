# Read-only Windows security baseline check. It changes nothing.
# Usage: powershell -NoProfile -ExecutionPolicy Bypass -File .\Check-WindowsSecurity.ps1 [-Html report.html]
param([string]$Html = "")

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$results = New-Object System.Collections.Generic.List[object]

function Add-Result($Item, $Value, $Status, $Advice) {
    if ($Status -eq "PASS") { $Advice = "-" }
    $results.Add([pscustomobject]@{ Item = $Item; Value = "$Value"; Status = $Status; Advice = $Advice })
}

function Test-Check($Item, [scriptblock]$Block) {
    try { & $Block }
    catch { Add-Result $Item "unreadable" "WARN" "Run in an elevated PowerShell, or this feature is not available." }
}

Test-Check "Defender real-time protection" {
    $mp = Get-MpComputerStatus
    $s = if ($mp.RealTimeProtectionEnabled) { "PASS" } else { "FAIL" }
    Add-Result "Defender real-time protection" $mp.RealTimeProtectionEnabled $s "Turn on real-time protection in Windows Security."
    $age = [int]((Get-Date) - $mp.AntivirusSignatureLastUpdated).TotalDays
    $s = if ($age -le 3) { "PASS" } elseif ($age -le 7) { "WARN" } else { "FAIL" }
    Add-Result "Defender signature age (days)" $age $s "Update signatures: Windows Security > Virus & threat protection updates."
    $s = if ($mp.IsTamperProtected) { "PASS" } else { "WARN" }
    Add-Result "Defender tamper protection" $mp.IsTamperProtected $s "Turn on tamper protection so malware cannot disable Defender."
}

Test-Check "Firewall" {
    foreach ($p in Get-NetFirewallProfile) {
        $s = if ($p.Enabled) { "PASS" } else { "FAIL" }
        Add-Result ("Firewall " + $p.Name + " profile") $p.Enabled $s "Turn the profile on unless another firewall product manages it."
    }
}

Test-Check "UAC" {
    $v = (Get-ItemProperty "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System").EnableLUA
    $s = if ($v -eq 1) { "PASS" } else { "FAIL" }
    Add-Result "UAC (EnableLUA)" $v $s "Set EnableLUA to 1 and reboot."
}

Test-Check "SMB" {
    $smb = Get-SmbServerConfiguration
    $s = if (-not $smb.EnableSMB1Protocol) { "PASS" } else { "FAIL" }
    Add-Result "SMBv1 server" $smb.EnableSMB1Protocol $s "Disable SMBv1. It is the protocol abused by worms such as WannaCry."
    $s = if ($smb.RequireSecuritySignature) { "PASS" } else { "WARN" }
    Add-Result "SMB signing required" $smb.RequireSecuritySignature $s "Require SMB signing to block relay attacks."
}

Test-Check "BitLocker" {
    $vol = Get-BitLockerVolume -MountPoint $env:SystemDrive
    $s = if ($vol.ProtectionStatus -eq "On") { "PASS" } else { "WARN" }
    Add-Result ("BitLocker " + $vol.MountPoint) $vol.ProtectionStatus $s "Encrypt the system drive if the device can be lost or stolen."
}

Test-Check "RDP" {
    $v = (Get-ItemProperty "HKLM:\SYSTEM\CurrentControlSet\Control\Terminal Server").fDenyTSConnections
    $on = ($v -eq 0)
    $s = if ($on) { "WARN" } else { "PASS" }
    Add-Result "Remote Desktop enabled" $on $s "Turn off Remote Desktop unless needed. If needed, require NLA and restrict the source."
}

Test-Check "Secure Boot" {
    $sb = Confirm-SecureBootUEFI
    $s = if ($sb) { "PASS" } else { "WARN" }
    Add-Result "Secure Boot" $sb $s "Enable Secure Boot in UEFI settings."
}

Test-Check "Guest account" {
    $g = Get-LocalUser | Where-Object { $_.SID.Value -like "*-501" }
    $s = if (-not $g.Enabled) { "PASS" } else { "FAIL" }
    Add-Result "Guest account enabled" $g.Enabled $s "Disable the built-in Guest account."
}

Test-Check "AutoLogon" {
    $v = (Get-ItemProperty "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon").AutoAdminLogon
    $on = ($v -eq "1")
    $s = if ($on) { "FAIL" } else { "PASS" }
    Add-Result "Automatic sign-in" $on $s "Turn off automatic sign-in. It stores credentials on the machine."
}

$results | Format-Table Item, Value, Status -AutoSize

$count = $results | Group-Object Status | ForEach-Object { $_.Name + "=" + $_.Count }
Write-Output ("Summary: " + ($count -join "  "))

if ($Html -ne "") {
    $os = (Get-CimInstance Win32_OperatingSystem).Caption
    $rows = foreach ($r in $results) {
        $cls = $r.Status.ToLower()
        "<tr class='$cls'><td>$($r.Item)</td><td>$($r.Value)</td><td><b>$($r.Status)</b></td><td>$($r.Advice)</td></tr>"
    }
    $page = @"
<!doctype html><meta charset="utf-8"><title>Windows security baseline</title>
<style>
body{font:15px Segoe UI,sans-serif;margin:24px;color:#222}
h1{font-size:20px}
table{border-collapse:collapse;width:100%}
th,td{border:1px solid #ccc;padding:6px 10px;text-align:left}
th{background:#f0f0f0}
tr.pass td:nth-child(3){color:#0a7a2f}
tr.warn td:nth-child(3){color:#b26a00}
tr.fail td:nth-child(3){color:#c00}
tr.fail{background:#fff0f0}
tr.warn{background:#fff8e8}
</style>
<h1>Windows security baseline ($os)</h1>
<p>$($count -join " / ")</p>
<table><tr><th>Item</th><th>Value</th><th>Status</th><th>What to do</th></tr>
$($rows -join "`n")
</table>
"@
    Set-Content -Path $Html -Value $page -Encoding UTF8
    Write-Output "Report written: $Html"
}
