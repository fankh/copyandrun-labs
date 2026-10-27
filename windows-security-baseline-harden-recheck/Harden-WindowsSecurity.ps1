# Fixes the settings that Check-WindowsSecurity.ps1 reports as FAIL or WARN.
# Without -Apply it only prints what it would change. With -Apply it changes the settings.
# Run in an elevated PowerShell. Test on a VM first.
param([switch]$Apply)

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

function Step($Text, [scriptblock]$Do) {
    if ($Apply) {
        try { & $Do; Write-Output ("DONE    " + $Text) }
        catch { Write-Output ("FAILED  " + $Text + " : " + $_.Exception.Message) }
    } else {
        Write-Output ("PLAN    " + $Text)
    }
}

Step "Turn on Windows Firewall for Domain, Private, Public" {
    Set-NetFirewallProfile -Profile Domain, Private, Public -Enabled True
}
Step "Turn off Remote Desktop" {
    Set-ItemProperty "HKLM:\SYSTEM\CurrentControlSet\Control\Terminal Server" -Name fDenyTSConnections -Value 1
}
Step "Disable SMBv1 server" {
    Set-SmbServerConfiguration -EnableSMB1Protocol $false -Force
}
Step "Require SMB signing" {
    Set-SmbServerConfiguration -RequireSecuritySignature $true -Force
}
Step "Disable the built-in Guest account" {
    Disable-LocalUser -Name Guest
}
Step "Turn off automatic sign-in" {
    Set-ItemProperty "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" -Name AutoAdminLogon -Value "0"
}

if (-not $Apply) { Write-Output "Nothing changed. Run again with -Apply to make these changes." }
