# LAB ONLY. Creates a temporary local account and a few harmless failed logons in a disposable test VM.
# Stays below the lockout threshold. The password below is a throwaway example, not a real password.
# Never try wrong passwords on a real account: that can lock it out.
param([ValidateSet("Local", "Network", "Unknown")][string]$Phase = "Local", [int]$Count = 4)

$tmpUser = "labtest"
$tmpPass = "Tmp-Only-8842!"
$wrong   = "Wrong-Guess-1!"

if (-not (Get-LocalUser -Name $tmpUser -ErrorAction SilentlyContinue)) {
    $sec = ConvertTo-SecureString $tmpPass -AsPlainText -Force
    New-LocalUser -Name $tmpUser -Password $sec -Description "temporary lab account" | Out-Null
    Write-Output "Created temporary account: $tmpUser"
}

Add-Type -Namespace Lab -Name Native -MemberDefinition @"
[System.Runtime.InteropServices.DllImport("advapi32.dll", SetLastError = true, CharSet = System.Runtime.InteropServices.CharSet.Unicode)]
public static extern bool LogonUser(string user, string domain, string pass, int type, int provider, out System.IntPtr token);
"@

function Try-Local($user, $pass) {
    $t = [System.IntPtr]::Zero
    [void][Lab.Native]::LogonUser($user, $env:COMPUTERNAME, $pass, 2, 0, [ref]$t)
}

switch ($Phase) {
    "Local" {
        1..$Count | ForEach-Object { Try-Local $tmpUser $wrong }
        Write-Output "Phase Local: $Count interactive failures (type 2) for $tmpUser"
    }
    "Network" {
        # Windows logs a repeated failure to the same server name only once, so use two different addresses.
        foreach ($h in "localhost", "127.0.0.1") {
            net use \\$h\IPC$ /user:$tmpUser $wrong 2>&1 | Out-Null
        }
        Write-Output "Phase Network: 2 network failures (type 3) for $tmpUser"
    }
    "Unknown" {
        foreach ($n in "ghostuser1", "ghostuser2", "ghostuser3") {
            net use \\localhost\IPC$ /user:$n $wrong 2>&1 | Out-Null
        }
        Write-Output "Phase Unknown: 3 attempts with names that do not exist"
    }
}
