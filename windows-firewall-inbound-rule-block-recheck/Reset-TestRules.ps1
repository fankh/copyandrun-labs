# Removes the cr-test firewall rules created in this note and stops the test listener.
# Usage (elevated PowerShell): powershell -NoProfile -ExecutionPolicy Bypass -File .\Reset-TestRules.ps1
Get-NetFirewallRule -DisplayName 'cr-test*' -ErrorAction SilentlyContinue | Remove-NetFirewallRule
Get-CimInstance Win32_Process -Filter "Name='powershell.exe'" |
    Where-Object { $_.CommandLine -match 'Start-TestListener' } |
    ForEach-Object { Stop-Process -Id $_.ProcessId -Force }
Write-Output ("cr-test rules left: {0}" -f @(Get-NetFirewallRule -DisplayName 'cr-test*' -ErrorAction SilentlyContinue).Count)
