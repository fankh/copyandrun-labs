# LAB ONLY. Removes the temporary account and restores the lockout policy used in this lab.
param([int]$LockoutThreshold = 10)
net use \\localhost\IPC$ /delete 2>&1 | Out-Null
if (Get-LocalUser -Name labtest -ErrorAction SilentlyContinue) { Remove-LocalUser -Name labtest; Write-Output "Removed labtest" }
net accounts /lockoutthreshold:$LockoutThreshold | Out-Null
Write-Output "Lockout threshold restored to $LockoutThreshold"
