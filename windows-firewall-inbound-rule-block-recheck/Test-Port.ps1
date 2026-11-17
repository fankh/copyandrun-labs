# Connects to a TCP port and reports the result. Without -Target it uses this computer's own (non-loopback) IPv4 address.
# Usage (PowerShell): .\Test-Port.ps1 -Port 8088 [-Target 169.254.10.10] [-TimeoutMs 2000]
param([int]$Port = 8088, [string]$Target = "", [int]$TimeoutMs = 2000)

if ($Target) {
    $ip = $Target
} else {
    $ip = (Get-NetIPAddress -AddressFamily IPv4 |
           Where-Object { $_.IPAddress -ne '127.0.0.1' } |
           Select-Object -First 1).IPAddress
}

$client = New-Object System.Net.Sockets.TcpClient
try {
    $task = $client.ConnectAsync($ip, $Port)
    if ($task.Wait($TimeoutMs) -and $client.Connected) {
        $client.GetStream().ReadTimeout = $TimeoutMs
        $reader = New-Object System.IO.StreamReader($client.GetStream())
        Write-Output ("Port {0}: CONNECTED, reply: {1}" -f $Port, $reader.ReadLine())
    } else {
        Write-Output ("Port {0}: no answer within {1} ms" -f $Port, $TimeoutMs)
    }
} catch {
    Write-Output ("Port {0}: FAILED at once (refused or stopped locally)" -f $Port)
}
$client.Close()
