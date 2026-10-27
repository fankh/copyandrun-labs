# LAB ONLY. Makes a disposable test VM less secure on purpose so the check has something to find.
# Never run this on a real PC. Run in an elevated PowerShell inside the VM.
Set-NetFirewallProfile -Profile Private, Public -Enabled False
Set-ItemProperty "HKLM:\SYSTEM\CurrentControlSet\Control\Terminal Server" -Name fDenyTSConnections -Value 0
Set-SmbServerConfiguration -RequireSecuritySignature $false -Force
Enable-LocalUser -Name Guest
Write-Output "Lab VM weakened: firewall (Private, Public) off, RDP on, SMB signing off, Guest on"
