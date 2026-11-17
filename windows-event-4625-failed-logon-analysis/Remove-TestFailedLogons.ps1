# Removes the temporary account and restores the lockout policy changed by this test.
param([int]$LockoutThreshold = 10)
net use \\localhost\IPC$ /delete 2>&1 | Out-Null
if (Get-LocalUser -Name cr-test -ErrorAction SilentlyContinue) { Remove-LocalUser -Name cr-test; Write-Output "Removed cr-test" }
net accounts /lockoutthreshold:$LockoutThreshold | Out-Null
Write-Output "Lockout threshold restored to $LockoutThreshold"
