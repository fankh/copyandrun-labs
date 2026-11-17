# Read-only check: firewall profiles, TCP listeners on the given ports, the inbound rules that match them,
# and the Filtering Platform audit settings. It changes nothing.
# Usage (elevated PowerShell): powershell -NoProfile -ExecutionPolicy Bypass -File .\Check-Firewall.ps1 -Ports 8088
param([int[]]$Ports = @(8088))

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Output "== Profiles"
foreach ($p in Get-NetFirewallProfile) {
    $inbound = if ($p.DefaultInboundAction -eq 'NotConfigured') { 'NotConfigured (Windows default: Block)' } else { "$($p.DefaultInboundAction)" }
    Write-Output ("  {0,-8} Enabled={1,-5} DefaultInbound={2}" -f $p.Name, $p.Enabled, $inbound)
}

Write-Output ""
Write-Output "== Listeners and matching inbound rules"
$results = foreach ($port in $Ports) {
    $listen = @(Get-NetTCPConnection -State Listen -LocalPort $port -ErrorAction SilentlyContinue)
    $rules  = @(Get-NetFirewallPortFilter -Protocol TCP |
                Where-Object { $_.LocalPort -contains "$port" } |
                Get-NetFirewallRule |
                Where-Object { $_.Direction -eq 'Inbound' -and $_.Enabled -eq 'True' })
    [pscustomobject]@{ Port = $port; Listen = $listen; Rules = $rules }
}
foreach ($r in $results) {
    if ($r.Listen.Count -eq 0) {
        Write-Output ("  TCP {0}: not listening" -f $r.Port)
    } else {
        $proc = (Get-Process -Id $r.Listen[0].OwningProcess).ProcessName
        Write-Output ("  TCP {0}: listening on {1} ({2})" -f $r.Port, $r.Listen[0].LocalAddress, $proc)
    }
    if ($r.Rules.Count -eq 0) {
        Write-Output "    rules: none"
    } else {
        foreach ($rule in $r.Rules) {
            Write-Output ("    rule : {0} / {1} / profile {2}" -f $rule.DisplayName, $rule.Action, $rule.Profile)
        }
    }
}

Write-Output ""
Write-Output "== Audit"
$packetDrop = (auditpol /get /subcategory:'{0CCE9225-69AE-11D9-BED3-505054503030}' /r | ConvertFrom-Csv).'Inclusion Setting'
$connection = (auditpol /get /subcategory:'{0CCE9226-69AE-11D9-BED3-505054503030}' /r | ConvertFrom-Csv).'Inclusion Setting'
Write-Output ("  Filtering Platform Packet Drop (5152): {0}" -f $packetDrop)
Write-Output ("  Filtering Platform Connection (5156/5157): {0}" -f $connection)

Write-Output ""
foreach ($r in $results) {
    if ($r.Listen.Count -eq 0) { continue }
    $block = @($r.Rules | Where-Object { $_.Action -eq 'Block' }).Count
    $allow = @($r.Rules | Where-Object { $_.Action -eq 'Allow' }).Count
    if ($block -gt 0)     { Write-Output ("Verdict TCP {0}: BLOCKED by a rule. A block rule wins over allow rules." -f $r.Port) }
    elseif ($allow -gt 0) { Write-Output ("Verdict TCP {0}: ALLOWED by a rule." -f $r.Port) }
    else                  { Write-Output ("Verdict TCP {0}: NO RULE. Remote access depends on the profile default only." -f $r.Port) }
}
