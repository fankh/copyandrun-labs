# Opens a TCP listener on one port and answers every connection with a short line, then exits after -Seconds.
# Usage (PowerShell): .\Start-TestListener.ps1 -Port 8088 -Seconds 600
param([int]$Port = 8088, [int]$Seconds = 600)

$listener = New-Object System.Net.Sockets.TcpListener([System.Net.IPAddress]::Any, $Port)
$listener.Start()
Write-Output ("Listening on 0.0.0.0:{0} for {1} seconds" -f $Port, $Seconds)

$end = (Get-Date).AddSeconds($Seconds)
while ((Get-Date) -lt $end) {
    if ($listener.Pending()) {
        $client = $listener.AcceptTcpClient()
        $bytes  = [System.Text.Encoding]::ASCII.GetBytes("cr-test ok`r`n")
        $client.GetStream().Write($bytes, 0, $bytes.Length)
        $client.Close()
    } else {
        Start-Sleep -Milliseconds 200
    }
}
$listener.Stop()
