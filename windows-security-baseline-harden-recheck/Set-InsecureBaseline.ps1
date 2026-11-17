# Weakens four settings on purpose so the check has something to find.
# Run in an elevated PowerShell, then restore with Harden-WindowsSecurity.ps1 -Apply.
Set-NetFirewallProfile -Profile Private, Public -Enabled False
Set-ItemProperty "HKLM:\SYSTEM\CurrentControlSet\Control\Terminal Server" -Name fDenyTSConnections -Value 0
Set-SmbServerConfiguration -RequireSecuritySignature $false -Force
Enable-LocalUser -Name Guest
Write-Output "Settings weakened: firewall (Private, Public) off, RDP on, SMB signing off, Guest on"
